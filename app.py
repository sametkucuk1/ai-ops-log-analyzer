import logging
import random
import time
import sys

# Log ayarları (Terminal ekranına anında basılması için)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("LogWhisperer")

ERROR_MESSAGES = [
    "Database connection timeout after 3000ms.",
    "Failed to flush redis cache: Out of memory.",
    "User authentication failed: Invalid token signature.",
    "Internal Server Error: NullPointerException in user_service.py:42",
    "API gateway routing error: Service unavailable."
]

logger.info("LogWhisperer App has started successfully!")

while True:
    dice = random.random()
    
    if dice < 0.10:
        logger.error(random.choice(ERROR_MESSAGES))
    elif dice < 0.15:
        logger.critical("SYSTEM CRASH: Core memory dump failed. Unrecoverable state!")
    else:
        logger.info(f"Healthy request processed. Response time: {random.randint(10, 150)}ms")
        
    time.sleep(2)
