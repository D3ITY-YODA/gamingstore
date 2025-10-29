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

# Database configuration - Render PostgreSQL with fallback
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Fallback to SQLite if no DATABASE_URL (for initial deployment)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    print("WARNING: Using SQLite database. Set DATABASE_URL for PostgreSQL.")

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-production')
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# Media files (use local storage for now)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

print("Render production settings loaded")
