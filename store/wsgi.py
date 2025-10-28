import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings.dev')
application = get_wsgi_application()
import os; print('=== SETTINGS MODULE ===', os.environ.get('DJANGO_SETTINGS_MODULE'))
