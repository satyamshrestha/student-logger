from utils.logger import logger

def log_action(action: str):
    logger.info(f"AUDIT: {action}")