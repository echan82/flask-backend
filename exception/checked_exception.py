from model.model_sample import Failure


class CheckedException(Exception):
    def __init__(self, error_message, http_status_code, error_code=None):
        Exception.__init__(self)
        self.error_message = error_message
        self.http_status_code = http_status_code
        if error_code is not None:
            self.error_code = error_code

    def get_response(self):
        failure = Failure()
        failure.error_message = self.error_message
        if hasattr(self, 'error_code'):
            failure.error_code = self.error_code
        response = failure.dump(failure)
        return response, self.http_status_code
