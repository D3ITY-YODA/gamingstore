"""
Production settings for Azure deployment
"""
import os
from .base import *

# Debug mode off
DEBUG = False

# Azure will provide the hostname
ALLOWED_HOSTS = [os.environ.get('WEBSITE_HOSTNAME', 'localhost'), '127.0.0.1']

# Database configuration - Azure PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', '') + '@' + os.environ.get('DB_HOST', '').split('.')[0],
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key-here')
CSRF_TRUSTED_ORIGINS = [f"https://{os.environ.get('WEBSITE_HOSTNAME', 'localhost')}"]

# DON'T modify MIDDLEWARE here - use what's imported from base.py
# Just ensure WhiteNoise storage is set
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Azure Storage for media files (optional)
if os.environ.get('AZURE_ACCOUNT_NAME'):
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
    AZURE_CONTAINER = 'media'

# Ensure we have all required middleware by not overriding the imported MIDDLEWARE
print("Production settings loaded - using middleware from base settings")
