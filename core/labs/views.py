from django.shortcuts import render
from .models import Product, Category, Order  # Обов'язково додай Order сюди!

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'title': 'Streethouse - Головна',
        'categories': categories,
        'products': products,
    }
    return render(request, 'labs/index.html', context)

def about(request):
    categories = Category.objects.all()
    context = {
        'title': 'Про проект STREETHOUSE',
        'categories': categories,
    }
    return render(request, 'labs/about.html', context)

def orders_list(request):
    orders = Order.objects.all()
    categories = Category.objects.all()
    context = {
        'title': 'Мої замовлення',
        'orders': orders,
        'categories': categories,
    }
    return render(request, 'labs/orders.html', context)