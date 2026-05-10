from utils.logger import logger
import time

def send_welcome_email(username: str):
    time.sleep(5) # Simulating email sending.

    logger.info(f"Sent welcome email to {username}!")