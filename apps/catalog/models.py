# apps/catalog/models.py
from django.db import models
from django.core.validators import MinValueValidator

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    shipping_days_min = models.IntegerField(default=7)
    shipping_days_max = models.IntegerField(default=21)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('FINGER_SLEEVES', '📱 Finger Sleeves'),
        ('MOBILE_ACCESSORIES', '📱 Mobile Accessories'),
        ('GAMING_MICE', '🖱️ Gaming Mice'),
        ('KEYBOARDS', '⌨️ Keyboards'),
        ('HEADSETS', '🎧 Headsets'),
        ('CONTROLLERS', '🎮 Controllers'),
        ('GAMING_CHAIRS', '💺 Gaming Chairs'),
        ('PC_GAMES', '🖥️ PC Games'),
    ]
    
    # Basic product info
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    # Dropshipping pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Supplier info
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    supplier_product_id = models.CharField(max_length=100, blank=True)
    supplier_url = models.URLField(blank=True)
    
    # Inventory (always in stock for dropshipping)
    stock_quantity = models.IntegerField(default=999)
    is_dropshipping = models.BooleanField(default=True)
    
    # Images
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-calculate profit margin
        if self.cost_price and self.sale_price and self.cost_price > 0:
            self.profit_margin = ((self.sale_price - self.cost_price) / self.cost_price) * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} (Margin: {self.profit_margin}%)"