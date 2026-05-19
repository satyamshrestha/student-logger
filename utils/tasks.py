from utils.logger import logger
import time

def send_welcome_email(username: str):
    try:
        time.sleep(5) # Simulating email sending.
        print(f"Welcome email sent to {username}")

    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")