import time
from starlette.middleware.base import BaseHTTPMiddleware

from utils.logger import logger as base_logger
from utils.logging_adapter import RequestLoggerAdapter

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request_logger = RequestLoggerAdapter(
            base_logger,
            {"request_id": request.state.request_id}
        )

        start_time = time.time()

        request_logger.info(
            f"Incoming request: {request.method} {request.url}"
        )

        response = await call_next(request)

        duration = time.time() - start_time

        request_logger.info(
            f"Completed request: {request.method} {request.url} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.4f}s"
        )

        return response