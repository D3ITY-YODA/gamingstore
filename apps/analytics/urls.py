from django.urls import path
from . import views

urlpatterns = [
    path('profit-analytics/', views.profit_analytics, name='profit_analytics'),
]
