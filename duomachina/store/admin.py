from django.contrib import admin
from .models import Product, Order, OrderItem, Commission

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price',)

class CommissionInline(admin.TabularInline):
    model = Commission
    extra = 0
    readonly_fields = ('amount', 'created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'price', 'product_type', 'created_at')
    list_filter = ('product_type', 'artist', 'created_at')
    search_fields = ('name', 'description', 'artist__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'total_price')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__is_paid', 'product__product_type')
    search_fields = ('order__user__username', 'product__name')
    readonly_fields = ('price',)
    inlines = [CommissionInline]

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('artist', 'order_item', 'amount', 'created_at')
    list_filter = ('created_at', 'artist')
    search_fields = ('artist__username', 'order_item__product__name')
    readonly_fields = ('created_at', 'amount')
    ordering = ('-created_at',)
