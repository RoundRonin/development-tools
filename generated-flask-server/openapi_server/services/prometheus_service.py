import logging
import psutil
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry, REGISTRY
from flask import Response
from concurrent.futures import ThreadPoolExecutor
from ..config.logging_handler import setup_logging

logger = setup_logging()

# Create a custom registry to avoid conflicts with the default global registry
registry = CollectorRegistry(auto_describe=True)

# Define metrics using the custom registry
REQUEST_COUNT = Counter('request_count', 'Total Request Count', ['method', 'endpoint', 'http_status'], registry=registry)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['method', 'endpoint'], registry=registry)
STATUS_CODE_COUNT = Counter('status_code_count', 'HTTP status codes', ['status_code'], registry=registry)
CPU_USAGE = Gauge('cpu_usage', 'CPU usage', registry=registry)
MEMORY_USAGE = Gauge('memory_usage', 'Memory usage', registry=registry)

executor = ThreadPoolExecutor(max_workers=5)

def async_record_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=None)
    memory_usage = psutil.virtual_memory().percent
    CPU_USAGE.set(cpu_usage)
    MEMORY_USAGE.set(memory_usage)
    logger.debug(f"Metrics recorded: CPU usage={cpu_usage}, Memory usage={memory_usage}")

def record_request_data(method, endpoint, status_code, duration):
    logger.debug(f"Recording request data: method={method}, endpoint={endpoint}, status_code={status_code}, duration={duration:.4f}")
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
    STATUS_CODE_COUNT.labels(status_code=status_code).inc()
    
    # Record system metrics asynchronously
    executor.submit(async_record_system_metrics)

def metrics():
    logger.debug("Generating metrics")
    return Response(generate_latest(registry), mimetype='text/plain')
