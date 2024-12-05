#!/usr/bin/env python3

import connexion
import time
import os
from flask import Flask, request
from flask_migrate import Migrate, init, migrate, upgrade
from werkzeug.serving import run_simple
from concurrent.futures import ThreadPoolExecutor
from openapi_server.services.prometheus_service import record_request_data, metrics
from openapi_server import encoder
from openapi_server.config.logging_handler import setup_logging
from openapi_server.config.tracing_handler import setup_tracing
from openapi_server.DAL.database import db
from openapi_server.config.config import Config
from openapi_server.services.error_handler import handle_errors

logger = setup_logging()
port = int(os.getenv('PYTHON_SERVER_PORT', 8080))

executor = ThreadPoolExecutor(max_workers=10)

def log_message(message):
    logger.info(message)

def async_log(message):
    executor.submit(log_message, message)

def create_app():
    connexion_app = connexion.App(__name__, specification_dir='./openapi/')
    connexion_app.add_api('openapi.yaml', arguments={'title': 'Articles API'}, pythonic_params=True)

    flask_app = connexion_app.app
    flask_app.json_encoder = encoder.JSONEncoder
    flask_app.config.from_object(Config)

    db.init_app(flask_app)
    setup_tracing(flask_app)

    @flask_app.before_request
    def start_timer():
        request.start_time = time.time()

    @flask_app.after_request
    def log_request(response):
        if not hasattr(request, 'start_time'):
            logger.error(f"Request start_time not set for request: {request.method} {request.path}")
            return response

        duration = time.time() - request.start_time
        async_log(f"Request completed: {request.method} {request.path} with status {response.status_code} in {duration:.4f} seconds")
        if request.endpoint != 'metrics':
            record_request_data(request.method, request.path, response.status_code, duration)
        return response

    @flask_app.route('/metrics')
    def metrics_endpoint():
        return metrics()

    return connexion_app, flask_app

connexion_app, app = create_app()

handle_errors(app)

migrate_extension = Migrate(app, db)

def initialize_database():
    with app.app_context():
        if not os.path.exists('migrations'):
            init(directory='migrations')
        else:
            logger.debug("Migrations directory already exists")
        migrate(directory='migrations', message='Initial migration.')
        upgrade(directory='migrations')

initialize_database()

if __name__ == '__main__':
    run_simple('0.0.0.0', port, app, use_reloader=True, reloader_type='watchdog')
