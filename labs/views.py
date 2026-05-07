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


from django.shortcuts import get_object_or_404  # Переконайся, що get_object_or_404 імпортовано зверху


def category_detail(request, pk):
    # Отримуємо конкретну категорію
    category = get_object_or_404(Category, pk=pk)
    # Фільтруємо товари: тільки ті, що належать цій категорії
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()  # Для навігаційного меню

    context = {
        'title': f'Категорія: {category.name}',
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'labs/category.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    categories = Category.objects.all()
    return render(request, 'labs/product_detail.html', {
        'product': product,
        'categories': categories,
        'title': product.name
    })