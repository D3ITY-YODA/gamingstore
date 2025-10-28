import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'  # Make sure this is set

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to True for development

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']  # Add this line

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your custom apps
    'apps.accounts',
    'apps.catalog',
    'apps.orders',
    'apps.payments',
    'apps.analytics',

    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',  # Must be before auth
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Must be after sessions
    'django.contrib.messages.middleware.MessageMiddleware',  # Must be after auth
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Your main templates directory
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.orders.context_processors.cart',  # Cart context processor
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Your static files directory
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where collectstatic puts files

# Media files (Uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Session settings for cart
CART_SESSION_ID = 'cart'


# Replace the Azure section with this safer version:

# Azure Production Settings
import os
if 'WEBSITE_HOSTNAME' in os.environ:  # Detect Azure environment
    print("=== AZURE PRODUCTION ENVIRONMENT DETECTED ===")
    
    # Production settings
    DEBUG = False
    ALLOWED_HOSTS = [
        os.environ['WEBSITE_HOSTNAME'],
        '127.0.0.1',
        'localhost'
    ]
    
    # Azure PostgreSQL Database
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
    
    # Static files configuration for Azure
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-azure')
    CSRF_TRUSTED_ORIGINS = [f"https://{os.environ['WEBSITE_HOSTNAME']}"]
    
    # WhiteNoise configuration (without modifying MIDDLEWARE)
    # Make sure WhiteNoise is already in your MIDDLEWARE in the correct position
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Azure Storage for media files
    if os.environ.get('AZURE_ACCOUNT_NAME'):
        DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
        AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
        AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
        AZURE_CONTAINER = 'media'ROOT_URLCONF = "store.urls"
