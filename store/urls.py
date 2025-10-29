from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.catalog.urls')),  # Catalog app handles main page
    path('orders/', include('apps.orders.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('payments/', include('apps.payments.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from apps.views import HealthCheck

urlpatterns = [
    path('health/', HealthCheck.as_view(), name='health_check'),
    # ... your existing URLs
]
