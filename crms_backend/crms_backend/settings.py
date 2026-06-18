import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Determine the environment (development or production)
DJANGO_ENV = os.getenv('DJANGO_ENV', '')

if DJANGO_ENV == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *