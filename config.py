from os import path

# BASIC SITE CONFIG
PROJECT_NAME = "OnlineShop"
COMPANY_NAME = "AlyExpress™"
SECRET_KEY = '<KEY>'
DEBUG = True

# SERVER CONFIG
HOST = '127.0.0.1'
PORT = 8080

# DIRECTORIES CONFIG
TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'
DATABASE_DIR = 'database'
DATABASE_PATH = path.join(DATABASE_DIR, "database.db")