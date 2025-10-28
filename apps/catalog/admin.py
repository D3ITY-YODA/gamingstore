from django.contrib import admin
from django import forms
from .models import Product, Supplier

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        cost_price = cleaned_data.get('cost_price')
        sale_price = cleaned_data.get('sale_price')
        
        # Auto-calculate sale price if only cost is provided
        if cost_price and not sale_price:
            margin_rates = {
                'FINGER_SLEEVES': 2.5,    # 250%
                'MOBILE_ACCESSORIES': 2.2,
                'GAMING_MICE': 1.8,
                'KEYBOARDS': 1.7,
                'HEADSETS': 1.7,
                'CONTROLLERS': 1.8,
                'GAMING_CHAIRS': 1.6,
                'PC_GAMES': 1.5,
            }
            category = cleaned_data.get('category')
            margin = margin_rates.get(category, 1.8)
            cleaned_data['sale_price'] = cost_price * margin
        
        return cleaned_data

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'category', 'cost_price', 'sale_price', 'profit_margin', 'supplier', 'stock_quantity']
    list_filter = ['category', 'supplier', 'is_dropshipping']
    search_fields = ['name', 'supplier_product_id']
    readonly_fields = ['profit_margin']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Pricing & Dropshipping', {
            'fields': ('cost_price', 'sale_price', 'profit_margin', 'is_dropshipping', 'stock_quantity')
        }),
        ('Supplier Info', {
            'fields': ('supplier', 'supplier_product_id', 'supplier_url')
        }),
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'shipping_days_min', 'shipping_days_max', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
