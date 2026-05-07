from django.urls import path
from labs import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('orders/', views.orders_list, name='orders'),

    # --- ДОДАЙ ЦІ РЯДКИ НИЖЧЕ ---

    # Шлях для категорії (наприклад, /category/1/)
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

    # Шлях для конкретного товару (наприклад, /product/5/)
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]