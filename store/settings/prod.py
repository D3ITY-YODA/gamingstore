"""
Production settings for Render deployment
"""
import os
from .base import *
import dj_database_url

# Debug mode off
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Render hostnames
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.onrender.com,localhost,127.0.0.1').split(',')

# Database configuration - Render PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# Media files (use local storage for now)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

print("Render production settings loaded")
