import os
from datetime import timedelta

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY","super-secret-key")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY","jwt-secret-key")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    DATABASE_URL = os.environ.get("DATABASE_URL")

    API_KEY = os.environ.get("API_KEY","threat-api-key")