from django.urls import path
from labs import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('orders/', views.orders_list, name='orders'), # Новий шлях
]