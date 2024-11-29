from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

def setup_tracing(app):
    # Setup tracer provider
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: "articles-api"})
        )
    )

    # Setup OTLP exporter
    otlp_exporter = OTLPSpanExporter(endpoint="tempo:4317", insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Optional: Setup console span exporter for debugging
    console_exporter = ConsoleSpanExporter()
    console_span_processor = BatchSpanProcessor(console_exporter)
    trace.get_tracer_provider().add_span_processor(console_span_processor)

    # Instrument Flask app
    FlaskInstrumentor().instrument_app(app, excluded_urls="/metrics")

    # Optional: Instrument logging to capture logs as spans
    LoggingInstrumentor().instrument(set_logging_format=True)

