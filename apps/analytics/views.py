from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order, OrderItem

@login_required
def profit_analytics(request):
    # Time periods
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # Total profit calculation - only count completed orders
    completed_orders = Order.objects.filter(status__in=['DELIVERED', 'SHIPPED'])
    total_revenue = completed_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Calculate total cost and profit
    total_cost = 0
    for order in completed_orders:
        for item in order.items.all():
            if hasattr(item.product, 'cost_price'):
                total_cost += float(item.product.cost_price) * item.quantity
    
    total_profit = total_revenue - total_cost
    
    # Recent orders
    recent_orders = Order.objects.filter(created_at__gte=last_month)
    
    # Top products
    top_products = OrderItem.objects.filter(
        order__status__in=['DELIVERED', 'SHIPPED']
    ).values('product__name').annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_sold')[:5]
    
    context = {
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'profit_margin_percentage': (total_profit / total_revenue * 100) if total_revenue > 0 else 0,
        'recent_orders_count': recent_orders.count(),
        'top_products': top_products,
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='PENDING').count(),
    }
    
    return render(request, 'analytics/dashboard.html', context)
