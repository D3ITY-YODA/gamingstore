# apps/orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('management/', views.order_management, name='order_management'),
    path('update-tracking/<int:order_id>/', views.update_tracking, name='update_tracking'),
    path('send-to-supplier/<int:order_id>/', views.send_to_supplier, name='send_to_supplier'),
    path('quick-buy/<int:product_id>/', views.quick_buy, name='quick_buy'),
]