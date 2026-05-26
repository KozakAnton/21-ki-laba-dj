import uuid
from collections import defaultdict
from decimal import Decimal
import random

from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Avg, Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import (
    CheckoutForm,
    NewsletterForm,
    RatingForm,
    RegisterForm,
    LoginForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm,
)
from .models import Product, Category, Order, NewsletterSubscriber, PasswordResetCode


User = get_user_model()


def get_categories():
    return Category.objects.all()

def group_orders(orders):
    grouped = {}

    for order in orders:
        key = order.order_number if order.order_number else f"old-{order.id}"

        if key not in grouped:
            grouped[key] = {
                "order_number": key,
                "customer_name": order.customer_name,
                "phone": order.phone,
                "email": order.email,
                "address": order.address,
                "created_at": order.created_at,
                "items": [],
                "total_quantity": 0,
                "total_sum": Decimal("0.00"),
            }

        grouped[key]["items"].append(order)
        grouped[key]["total_quantity"] += order.quantity
        grouped[key]["total_sum"] += order.total_price

    return list(grouped.values())


def index(request):
    categories = get_categories()
    products = Product.objects.all()

    context = {
        'title': 'Streethouse - Головна',
        'categories': categories,
        'products': products,
    }

    return render(request, 'labs/index.html', context)


def about(request):
    categories = get_categories()

    context = {
        'title': 'Про проект STREETHOUSE',
        'categories': categories,
        'products_count': Product.objects.count(),
        'categories_count': Category.objects.count(),
        'orders_count': Order.objects.count(),
    }

    return render(request, 'labs/about.html', context)


def orders_list(request):
    categories = get_categories()

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            orders = Order.objects.all().order_by("-created_at")
        else:
            orders = Order.objects.filter(user=request.user).order_by("-created_at")
    else:
        orders = Order.objects.none()

    grouped_orders = group_orders(orders)
    total_orders_sum = sum(order_group["total_sum"] for order_group in grouped_orders)

    context = {
        "title": "Мої замовлення",
        "categories": categories,
        "grouped_orders": grouped_orders,
        "total_orders_sum": total_orders_sum,
    }

    return render(request, "labs/orders.html", context)


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    categories = get_categories()

    context = {
        'title': f'Категорія: {category.name}',
        'category': category,
        'products': products,
        'categories': categories,
    }

    return render(request, 'labs/category.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = get_categories()

    average_rating = product.ratings.aggregate(avg=Avg('score'))['avg']
    ratings_count = product.ratings.count()

    context = {
        'product': product,
        'categories': categories,
        'title': product.name,
        'average_rating': average_rating,
        'ratings_count': ratings_count,
        'rating_form': RatingForm(),
    }

    return render(request, 'labs/product_detail.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        size = request.POST.get("size")
        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        if quantity > 99:
            quantity = 99

        if not size:
            messages.error(request, "Будь ласка, виберіть розмір товару.")
            return redirect('product_detail', pk=product.pk)

        cart = request.session.get("cart", {})

        item_key = f"{product.id}:{size}"

        if item_key in cart:
            cart[item_key]["quantity"] += quantity
        else:
            cart[item_key] = {
                "product_id": product.id,
                "size": size,
                "quantity": quantity,
            }

        request.session["cart"] = cart
        request.session.modified = True

        messages.success(request, "Товар додано у кошик.")
        return redirect('cart')

    return redirect('product_detail', pk=product.pk)


def cart_detail(request):
    categories = get_categories()
    cart = request.session.get("cart", {})

    cart_items = []
    total_sum = Decimal("0.00")

    for item_key, item in cart.items():
        product = Product.objects.filter(pk=item["product_id"]).first()

        if not product:
            continue

        quantity = item["quantity"]
        size = item["size"]
        total = product.price * quantity
        total_sum += total

        cart_items.append({
            "key": item_key,
            "product": product,
            "quantity": quantity,
            "size": size,
            "total": total,
        })

    initial_data = {}

    if request.user.is_authenticated:
        initial_data = {
            "customer_name": request.user.username,
            "email": request.user.email,
        }

    context = {
        "title": "Кошик",
        "categories": categories,
        "cart_items": cart_items,
        "total_sum": total_sum,
        "checkout_form": CheckoutForm(initial=initial_data),
    }

    return render(request, "labs/cart.html", context)


def remove_from_cart(request, item_key):
    cart = request.session.get("cart", {})

    if item_key in cart:
        del cart[item_key]
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Товар видалено з кошика.")

    return redirect("cart")


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Ваш кошик порожній.")
        return redirect("cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            customer_name = form.cleaned_data["customer_name"]
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]

            order_user = request.user if request.user.is_authenticated else None

            # Один номер для всіх товарів з одного оформлення кошика
            order_number = str(uuid.uuid4())[:8].upper()

            for item_key, item in cart.items():
                product = Product.objects.filter(pk=item["product_id"]).first()

                if product:
                    Order.objects.create(
                        user=order_user,
                        order_number=order_number,
                        customer_name=customer_name,
                        phone=phone,
                        email=email,
                        address=address,
                        product=product,
                        size=item["size"],
                        quantity=item["quantity"],
                    )

            request.session["cart"] = {}
            request.session.modified = True

            messages.success(request, "Замовлення успішно оформлено.")
            return redirect("orders")

    messages.error(request, "Перевірте правильність введених даних.")
    return redirect("cart")


def newsletter_subscribe(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]

            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={"name": name}
            )

            if created:
                messages.success(request, "Ви успішно підписалися на розсилку.")
            else:
                messages.info(request, "Цей email вже підписаний на розсилку.")

    return redirect(request.META.get("HTTP_REFERER", "index"))


def add_rating(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = RatingForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.save()

            messages.success(request, "Дякуємо за вашу оцінку.")
        else:
            messages.error(request, "Помилка. Перевірте форму оцінки.")

    return redirect("product_detail", pk=product.pk)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    categories = get_categories()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "Реєстрація успішна. Ви увійшли в акаунт.")
            return redirect("profile")
    else:
        form = RegisterForm()

    return render(request, "labs/register.html", {
        "title": "Реєстрація",
        "form": form,
        "categories": categories,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    categories = get_categories()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Ви успішно увійшли.")
            return redirect("profile")
    else:
        form = LoginForm()

    return render(request, "labs/login.html", {
        "title": "Вхід",
        "form": form,
        "categories": categories,
    })


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Ви вийшли з акаунта.")

    return redirect("index")


@login_required
def profile_view(request):
    categories = get_categories()

    if request.user.is_superuser or request.user.is_staff:
        orders = Order.objects.all().order_by("-created_at")
        profile_title = "Всі замовлення"
    else:
        orders = Order.objects.filter(
            Q(user=request.user) | Q(email__iexact=request.user.email)
        ).distinct().order_by("-created_at")

        profile_title = "Мої замовлення"

    grouped_orders = group_orders(orders)
    total_sum = sum((order_group["total_sum"] for order_group in grouped_orders), Decimal("0.00"))

    return render(request, "labs/profile.html", {
        "title": "Особистий кабінет",
        "categories": categories,
        "grouped_orders": grouped_orders,
        "profile_title": profile_title,
        "total_sum": total_sum,
    })


def password_reset_request_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    categories = get_categories()

    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email__iexact=email).first()

            if user:
                code = str(random.randint(100000, 999999))

                PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)

                PasswordResetCode.objects.create(
                    user=user,
                    code=code
                )

                send_mail(
                    subject="Код відновлення пароля STREETHOUSE",
                    message=f"Ваш код для відновлення пароля: {code}\nКод дійсний 15 хвилин.",
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                request.session["reset_email"] = email

            messages.success(request, "Якщо такий email існує, ми надіслали код для відновлення.")
            return redirect("password_reset_confirm")
    else:
        form = PasswordResetRequestForm()

    return render(request, "labs/password_reset_request.html", {
        "title": "Відновлення пароля",
        "form": form,
        "categories": categories,
    })


def password_reset_confirm_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    categories = get_categories()
    reset_email = request.session.get("reset_email", "")

    if request.method == "POST":
        form = PasswordResetConfirmForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data["code"]
            new_password = form.cleaned_data["new_password1"]

            user = User.objects.filter(email__iexact=reset_email).first()

            if not user:
                messages.error(request, "Email для відновлення не знайдено. Спробуйте ще раз.")
                return redirect("password_reset_request")

            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).order_by("-created_at").first()

            if not reset_code:
                messages.error(request, "Неправильний код.")
                return redirect("password_reset_confirm")

            if reset_code.is_expired():
                reset_code.is_used = True
                reset_code.save()

                messages.error(request, "Код застарів. Отримайте новий код.")
                return redirect("password_reset_request")

            user.set_password(new_password)
            user.save()

            reset_code.is_used = True
            reset_code.save()

            if "reset_email" in request.session:
                del request.session["reset_email"]

            messages.success(request, "Пароль успішно змінено. Тепер увійдіть з новим паролем.")
            return redirect("login")
    else:
        form = PasswordResetConfirmForm()

    return render(request, "labs/password_reset_confirm.html", {
        "title": "Новий пароль",
        "form": form,
        "categories": categories,
        "reset_email": reset_email,
    })
def categories_list(request):
    categories = Category.objects.all().order_by('name')

    context = {
        'title': 'Усі категорії',
        'categories': categories,
    }

    return render(request, 'labs/categories.html', context)