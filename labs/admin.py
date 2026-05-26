from django.contrib import admin
from .models import Category, Product, Order, NewsletterSubscriber, ProductRating, PasswordResetCode


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'user',
        'phone',
        'email',
        'product',
        'size',
        'quantity',
        'total_price',
        'created_at'
    )
    list_filter = ('created_at', 'product')
    search_fields = ('customer_name', 'phone', 'email', 'product__name', 'user__username')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer_name', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('product__name', 'customer_name')


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email', 'code')