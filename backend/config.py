import os
from dotenv import load_dotenv
from datetime import timedelta

# 載入環境變數
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'default_secret_key'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'default_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)  
