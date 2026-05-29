import logging

class RequestLoggerAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):

        request_id = self.extra.get("request_id", "N/A")

        kwargs["extra"] = {
            "request_id": request_id
        }

        return msg, kwargs