#(©)CodeXBotz

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# Configure logging first to capture any startup issues
LOG_FILE_NAME = "filesharingbot.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=10,
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Define LOGGER as the root logger
LOGGER = logging.getLogger(__name__)

def validate_config():
    """Validate all required configuration variables"""
    errors = []
    
    if not os.environ.get("TG_BOT_TOKEN"):
        errors.append("TG_BOT_TOKEN is missing")
    if not os.environ.get("APP_ID"):
        errors.append("APP_ID is missing")
    if not os.environ.get("API_HASH"):
        errors.append("API_HASH is missing")
    if not os.environ.get("CHANNEL_ID"):
        errors.append("CHANNEL_ID is missing")
    else:
        try:
            int(os.environ.get("CHANNEL_ID"))
        except ValueError:
            errors.append("CHANNEL_ID must be an integer")
    
    if errors:
        LOGGER.critical("Configuration errors detected:")
        for error in errors:
            LOGGER.critical(f" - {error}")
        raise ValueError("Invalid configuration. Please check environment variables.")

# Validate config before proceeding
validate_config()

# Bot token @Botfather
TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]

# Your API ID from my.telegram.org
APP_ID = int(os.environ["APP_ID"])

# Your API Hash from my.telegram.org
API_HASH = os.environ["API_HASH"]

# Your db channel Id
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

# Port
PORT = int(os.environ.get("PORT", "8080"))

# Database 
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")

# Force sub channel id (0 to disable)
try:
    FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "0"))
except ValueError:
    FORCE_SUB_CHANNEL = 0
    LOGGER.warning("Invalid FORCE_SUB_CHANNEL value, defaulting to 0")

JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", "").lower() == "true"

# Workers
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_PIC = os.environ.get("START_PIC", "")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")

# Admins list
ADMINS = []
try:
    admins_str = os.environ.get("ADMINS", "")
    if admins_str:
        ADMINS = [int(x.strip()) for x in admins_str.split(",") if x.strip().isdigit()]
except ValueError:
    LOGGER.warning("Invalid ADMINS list format. Using empty list.")

ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)  # Default admin
ADMINS = list(set(ADMINS))  # Remove duplicates

# Force sub message 
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE", 
    "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>"
)

# Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Protect content
PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', "False").lower() == "true"

# Auto delete settings
try:
    AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))
except ValueError:
    AUTO_DELETE_TIME = 0
    LOGGER.warning("Invalid AUTO_DELETE_TIME value, defaulting to 0")

AUTO_DELETE_MSG = os.environ.get(
    "AUTO_DELETE_MSG", 
    "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time."
)

AUTO_DEL_SUCCESS_MSG = os.environ.get(
    "AUTO_DEL_SUCCESS_MSG", 
    "Your file has been successfully deleted. Thank you for using our service. ✅"
)

# Channel button settings
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "").lower() == "true"

# Bot stats text
BOT_STATS_TEXT = os.environ.get(
    "BOT_STATS_TEXT", 
    "<b>BOT UPTIME</b>\n{uptime}"
)

# User reply text
USER_REPLY_TEXT = os.environ.get(
    "USER_REPLY_TEXT", 
    "❌Don't send me messages directly I'm only File Share bot!"
)

# Log configuration summary
LOGGER.info("Configuration loaded successfully")
LOGGER.info(f"Bot Token: {'set' if TG_BOT_TOKEN else 'not set'}")
LOGGER.info(f"Channel ID: {CHANNEL_ID}")
LOGGER.info(f"Force Sub Channel: {FORCE_SUB_CHANNEL if FORCE_SUB_CHANNEL else 'Disabled'}")
LOGGER.info(f"Admins: {ADMINS}")
LOGGER.info(f"Database: {DB_NAME}")
