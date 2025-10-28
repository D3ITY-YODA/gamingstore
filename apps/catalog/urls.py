from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category>/', views.product_list, name='product_list_by_category'),
    path('supplier-dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
]
