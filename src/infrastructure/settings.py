import os

from dotenv import load_dotenv

load_dotenv()

# DATABASE
DATABASE = {
    "connections": {
        "default": f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    },
    "apps": {
        "models": {
            "models": [
                "src.modules.moderation.models",
                "aerich.models",
                "src.modules.administration.models",
                "src.modules.automation.models",
                "src.modules.engagement.models"
            ],
            "default_connection": "default",
        }
    },
}

# DISCORD
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# IMGBB API KEY
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# RESERVOIR_API_KEY
RESERVOIR_API_KEY = os.getenv("RESERVOIR_API_KEY")

# INFURA PROJECT_ID
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
