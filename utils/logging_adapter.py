import logging

class RequestLoggerAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):

        request_id = self.extra.get("request_id", "N/A")

        return f"[{request_id}] {msg}", kwargs