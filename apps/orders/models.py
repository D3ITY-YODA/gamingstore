# apps/orders/models.py
from django.db import models
from apps.catalog.models import Product

class Order(models.Model):
    ORDER_STATUS = [
        ('PENDING', '⏳ Pending'),
        ('PROCESSING', '🔄 Processing'),
        ('SENT_TO_SUPPLIER', '📦 Sent to Supplier'),
        ('SHIPPED', '🚚 Shipped'),
        ('DELIVERED', '✅ Delivered'),
        ('CANCELLED', '❌ Cancelled'),
    ]
    
    # Customer info
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # Order info
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Dropshipping automation
    supplier_order_id = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    shipping_carrier = models.CharField(max_length=100, blank=True)
    order_sent_to_supplier = models.BooleanField(default=False)
    estimated_delivery = models.DateField(blank=True, null=True)
    
    def send_to_supplier(self):
        """Simulate sending order to supplier"""
        self.status = 'SENT_TO_SUPPLIER'
        self.order_sent_to_supplier = True
        self.supplier_order_id = f"SUP{self.id}{self.created_at.strftime('%Y%m%d')}"
        self.save()
        
        # Log the action
        OrderLog.objects.create(
            order=self,
            action='SENT_TO_SUPPLIER',
            notes=f"Order sent to supplier. Supplier Order ID: {self.supplier_order_id}"
        )
    
    def __str__(self):
        return f"Order {self.id} - {self.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class OrderLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.order.id} - {self.action} - {self.created_at}"