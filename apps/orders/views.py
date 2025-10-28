from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.catalog.models import Product
from .models import Order, OrderItem, OrderLog

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'quantity': 1,
            'price': str(product.sale_price),
            'name': product.name,
            'image': product.image.url if product.image else ''
        }
    
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, item in cart.items():
        item_total = int(item['quantity']) * float(item['price'])
        total_price += item_total
        cart_items.append({
            'product_id': product_id,
            **item,
            'total': item_total
        })
    
    return render(request, 'orders/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# DROPSHIPPING FEATURES

@login_required
def order_management(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/management.html', {'orders': orders})

@login_required
def update_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        shipping_carrier = request.POST.get('shipping_carrier')
        
        order.tracking_number = tracking_number
        order.shipping_carrier = shipping_carrier
        order.status = 'SHIPPED'
        order.save()
        
        OrderLog.objects.create(
            order=order,
            action='TRACKING_ADDED',
            notes=f"Tracking: {tracking_number} via {shipping_carrier}"
        )
        
        messages.success(request, f"Tracking number added for Order #{order.id}")
        return redirect('order_management')
    
    return render(request, 'orders/update_tracking.html', {'order': order})

@login_required
def send_to_supplier(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Send order to supplier
    order.send_to_supplier()
    
    messages.success(request, f"Order #{order.id} sent to supplier!")
    return redirect('order_management')

def quick_buy(request, product_id):
    # Add to cart and redirect to checkout
    cart_add(request, product_id)
    return redirect('checkout')
