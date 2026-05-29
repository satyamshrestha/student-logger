import logging
from utils.logging_formatter import RequestIDFormatter

handler = logging.StreamHandler()

formatter = RequestIDFormatter(
    "%(asctime)s - %(levelname)s - [Request ID: %(request_id)s] - %(message)s"
)

handler.setFormatter(formatter)

logger = logging.getLogger(__name__)

logger.addHandler(handler)

logger.setLevel(logging.INFO)