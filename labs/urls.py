from django.urls import path
from labs import views

urlpatterns = [
    path('', views.index, name='index'),

    # Сторінки сайту
    path('about/', views.about, name='about'),
    path('orders/', views.orders_list, name='orders'),
    path('categories/', views.categories_list, name='categories'),

    # Категорії та товари
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/rating/', views.add_rating, name='add_rating'),

    # Кошик
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:item_key>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),

    # Розсилка
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Авторизація
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Відновлення пароля
    path('password-reset/', views.password_reset_request_view, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),
]