#!/usr/bin/env python3

import logging
import connexion
import time
from flask import request
from .prometheus_service import record_request_data, metrics
from openapi_server import encoder

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
for handler in logger.handlers:
    handler.terminator = '\n'

def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Articles API'},
                pythonic_params=True)

    @app.app.before_request
    def start_timer():
        logger.debug(f"Starting timer for request: {request.method} {request.path}")
        request.start_time = time.time()

    @app.app.after_request
    def log_request(response):
        if not hasattr(request, 'start_time'):
            logger.error(f"Request start_time not set for request: {request.method} {request.path}")
            return response

        duration = time.time() - request.start_time
        logger.debug(f"Request completed: {request.method} {request.path} with status {response.status_code} in {duration:.4f} seconds")
        if request.endpoint != 'metrics':
            record_request_data(request.method, request.path, response.status_code, duration)
        return response

    @app.app.route('/metrics')
    def metrics_endpoint():
        logger.debug("Metrics endpoint called")
        return metrics()

    logger.debug("Running Flask app...")
    app.run(port=8080)

if __name__ == '__main__':
    main()
