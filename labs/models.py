from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta



class Category(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name="Назва категорії",
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яІіЇїЄєҐґA-Za-z0-9\s\-]+$',
                message="Назва категорії може містити тільки літери, цифри, пробіли та дефіс."
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категорія")
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/', verbose_name="Зображення", null=True, blank=True)

    available_sizes = models.CharField(
        max_length=100,
        default="S,M,L",
        verbose_name="Доступні розміри",
        help_text="Введіть розміри через кому без пробілів. Наприклад: XS,S,M,L"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def get_sizes_list(self):
        return [size.strip() for size in self.available_sizes.split(',') if size.strip()]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Користувач"
    )

    order_number = models.CharField(
        max_length=40,
        verbose_name="Номер замовлення",
        blank=True,
        default=""
    )

    customer_name = models.CharField(max_length=100, verbose_name="Ім'я покупця")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, default="")
    email = models.EmailField(verbose_name="Email", blank=True, default="")
    address = models.CharField(max_length=255, verbose_name="Адреса доставки", blank=True, default="")

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    size = models.CharField(max_length=20, verbose_name="Розмір", blank=True, default="")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Замовлення від {self.customer_name}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"


class NewsletterSubscriber(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я", blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата підписки")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Підписник розсилки"
        verbose_name_plural = "Підписники розсилки"


class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings", verbose_name="Товар")
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я")
    score = models.PositiveSmallIntegerField(
        choices=[
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ],
        verbose_name="Оцінка"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оцінки")

    def __str__(self):
        return f"{self.product.name} — {self.score}/5"

    class Meta:
        verbose_name = "Оцінка товару"
        verbose_name_plural = "Оцінки товарів"


class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Користувач"
    )
    code = models.CharField(max_length=6, verbose_name="Код")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    is_used = models.BooleanField(default=False, verbose_name="Використано")

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)

    def __str__(self):
        return f"{self.user.username} — {self.code}"

    class Meta:
        verbose_name = "Код відновлення пароля"
        verbose_name_plural = "Коди відновлення пароля"

