import logging
from logging.handlers import RotatingFileHandler

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = '5010'
OWNER_ID = 1246987713

MSG_EFFECT = 5046509860389126442

SHORT_URL = "vplink.in" # shortner url 
SHORT_API = "35591ad98834a002e1fe0b3b4acc6d84ef401782" 
SHORT_TUT = ""

# Bot Configuration
SESSION = "yato"
TOKEN = "8140166471:AAFdkSriTGvFD2voFjITUSrGjGozcyJU8XU"
API_ID = "27686895"
API_HASH = "0e996bd3891969ec5dfebf8bb3e39e94"
WORKERS = 5

DB_URI = "mongodb+srv://anihubbot:Anihub123@cluster0.tk16ay6.mongodb.net/?appName=Cluster0"
DB_NAME = "yato"

FSUBS = []  # Force Subscription Channels [channel_id, request_enabled, timer_in_minutes]
# Database Channel (Primary)
DB_CHANNEL = -1003654284775  # just put channel id dont add ""
# Multiple Database Channels (can be set via bot settings)
# DB_CHANNELS = {
#     "-1002595092736": {"name": "Primary DB", "is_primary": True, "is_active": True},
#     "-1001234567890": {"name": "Secondary DB", "is_primary": False, "is_active": True}
# }
# Auto Delete Timer (seconds)
AUTO_DEL = 300
# Admin IDs
ADMINS = [1246987713]
# Bot Settings
DISABLE_BTN = False
PROTECT = True

# Premium Access Settings
PREMIUM_ONLY_MODE = True  # Enable/disable premium-only access
UPI_ID = "paytmqrslhta2csqu@paytm"  # Your UPI ID
PAYMENT_QR = "https://graph.org/file/90fc99d53f517bca4bf81-346bf43a3a17b0a425.jpg"  # Google Pay/BharatPe QR code URL
PAYMENT_ADMIN = "@MissFilo_bot"  # Admin username for payment confirmation

# Premium Plans (duration_days: price_inr)
PREMIUM_PLANS = {
    7: 49,
    15: 89,
    30: 139,
    180: 299,  # 6 months
    365: 399   # 12 months
}

# Free Access Token Settings
FREE_ACCESS_ENABLED = True  # Enable/disable free token verification
TOKEN_VALIDITY_HOURS = 6  # How long token access lasts (in hours)
# Token verification uses its own shortlink (independent from file shortener)
TOKEN_SHORTLINK_URL = "vplink.in"  # Shortlink service for token verification
TOKEN_SHORTLINK_API = "35591ad98834a002e1fe0b3b4acc6d84ef401782"  # API key for token verification

# Messages Configuration
MESSAGES = {
    "START": "<b>⚡ Welcome to VIRAL VERSE !</b>\n\n<i>Your gateway to premium content, resources, and links shared by our community.</i>\n\n<b>🔥 Features:</b>\n• 📸 Browse posts with images, videos & audio\n• ❤️ React with emojis\n• 💬 Comment and engage with the community\n• 🔗 Share posts with friends\n\n\n<b>👇 Click the button below to open the app!</b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b>",
    "ABOUT": "<b><blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/Anihubyt25'>Cʟɪᴄᴋ ʜᴇʀᴇ</a> \n›› ᴏᴡɴᴇʀ: @Anihubyt25\n›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a> \n›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a> \n›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a> \n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @Anihubyt25</b></blockquote>",
    "REPLY": "<b>For More Join - @Anihubyt25</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ {first}, \n\n‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ ‼️\n\n ⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",
    "START_PHOTO": "https://graph.org/file/8c1586a79388f0a74fa83-8c0e212b265e207a9c.jpg",
    "FSUB_PHOTO": "https://graph.org/file/8c1586a79388f0a74fa83-8c0e212b265e207a9c.jpg",
    "SHORT_PIC": "https://graph.org/file/8c1586a79388f0a74fa83-8c0e212b265e207a9c.jpg",
    "SHORT": "https://graph.org/file/8c1586a79388f0a74fa83-8c0e212b265e207a9c.jpg"
}

def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
