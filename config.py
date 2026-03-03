import os

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    DATABASE = "database.db"
    MODEL_PATH = "phishing_model.pkl"