from flask import jsonify

def handle_errors(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        status_code = 500
        if hasattr(e, 'code'):
            status_code = e.code

        response = {
            "error": str(e),
            "message": "An error occurred while processing your request."
        }

        app.logger.error(f"Error: {e}")

        return jsonify(response), status_code

    return app
