#!/usr/bin/python

from flask import Flask, json, request ,g
from api import api_bp
from exception.checked_exception import CheckedException
from exception.runtime_exception import RuntimeException
from util.flask_env import Environments
import log
import logging
import time


def create_app():
    app = Flask(__name__)
    env = Environments(app)
    env.from_yaml('config.yml')
    app.register_blueprint(api_bp, url_prefix='/v1')
    return app


if __name__ == '__main__':

    app = create_app()
    logger = logging.getLogger(__name__)

    @app.errorhandler(CheckedException)
    def handle_checked_exception(error):
        response, http_status_code = error.get_response()
        response = json.dumps(response.data, ensure_ascii=False)
        return response, http_status_code

    @app.errorhandler(RuntimeException)
    def handle_runtime_exception(error):
        response, http_status_code = error.get_response()
        response = json.dumps(response.data, ensure_ascii=False)
        return response, http_status_code
   
    @app.before_request
    def before_request():
        logger.debug('in before request')
        g.start = int(round(time.time() * 1000))

    @app.after_request
    def after_request(response):
        logger.debug('in after request')
        elapsed_time = int(round(time.time() * 1000)) - g.start
        logger.debug('%sms',elapsed_time)
        return response


    app.run(host="0.0.0.0", debug=True)
