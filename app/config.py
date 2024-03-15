import os


# App config
SECRET_KEY = os.environ.get("SECRET_KEY", "learn_hub_$$568fas4")
DEBUG = os.environ.get("DEBUG", "False") == "True"

# JWT config
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
REFRESH_SECRET = os.environ.get("REFRESH_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

# Media config
MEDIA_ROOT: str = "media"
MEDIA_URL: str = "/media/"
