from .base import *
import os
from datetime import timedelta

DEBUG = False


SECRET_KEY = os.getenv("SECRET_KEY")


ALLOWED_HOSTS = [
    "crms.tomcaliento.com",
    "www.crms.tomcaliento.com",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "https://crms.tomcaliento.com",
    "https://www.crms.tomcaliento.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://crms.tomcaliento.com",
    "https://www.crms.tomcaliento.com",
]

# Application definition
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
    'ROTATE_REFRESH_TOKENS': False,
     'SIGNING_KEY': SECRET_KEY,
}