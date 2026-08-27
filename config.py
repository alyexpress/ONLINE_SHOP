from os import path

# BASIC SITE CONFIG
PROJECT_NAME = "OnlineShop"
COMPANY_NAME = "AlyExpress™"
SECRET_KEY = '<KEY>'
DEBUG = True

# SERVER CONFIG
HOST = '0.0.0.0'
PORT = 8080

# DIRECTORIES CONFIG
TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'
DATABASE_DIR = 'database'
DATABASE_PATH = path.join(DATABASE_DIR, "database/database.db")
COVER_DIR = path.join(STATIC_DIR, "cover")

# COOKIES CONFIG
CART_COOKIES = "product_"
EXPIRES_COOKIES = 60 * 60 * 24 * 30  # 1 month