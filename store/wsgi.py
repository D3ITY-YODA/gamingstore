import os
from django.core.wsgi import get_wsgi_application

# FORCE production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings.prod')
application = get_wsgi_application()
