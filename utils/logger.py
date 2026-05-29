import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [Request ID: %(request_id)s] - %(message)s"
)

logger = logging.getLogger(__name__)