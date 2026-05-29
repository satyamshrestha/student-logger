import logging

class RequestIDFormatter(logging.Formatter):

    def format(self, record):

        if not hasattr(record, "request_id"):
            record.request_id = "N/A"

        return super().format(record)