# apps/catalog/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Supplier
from apps.orders.models import Order

def product_list(request):
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    products = Product.objects.all()
    
    if category:
        products = products.filter(category=category)
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    context = {
        'products': products,
        'categories': Product.CATEGORY_CHOICES,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'catalog/product_detail.html', {'product': product})

@login_required
def supplier_dashboard(request):
    suppliers = Supplier.objects.filter(is_active=True)
    supplier_data = []
    
    for supplier in suppliers:
        products_count = Product.objects.filter(supplier=supplier).count()
        orders_count = Order.objects.filter(
            items__product__supplier=supplier
        ).distinct().count()
        
        supplier_data.append({
            'supplier': supplier,
            'products_count': products_count,
            'orders_count': orders_count,
        })
    
    context = {
        'supplier_data': supplier_data,
        'total_products': Product.objects.count(),
        'total_suppliers': suppliers.count(),
    }
    return render(request, 'catalog/supplier_dashboard.html', context)