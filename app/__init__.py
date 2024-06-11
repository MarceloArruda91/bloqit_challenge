import logging

from flask import Flask, redirect, jsonify
from flasgger import Swagger

from app.logging_config import setup_logging
from app.routes import api


def create_app():
    app = Flask(__name__)
    setup_logging()
    app.register_blueprint(api, url_prefix="/api")
    swagger = Swagger(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        response = jsonify({"error": str(e)})
        response.status_code = 500
        return response

    @app.route("/")
    def index():
        return redirect("/apidocs")

    return app
