from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
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

    # Нове поле для розмірів
    available_sizes = models.CharField(
        max_length=100,
        default="S,M,L",
        verbose_name="Доступні розміри",
        help_text="Введіть розміри через кому без пробілів (наприклад: XS,S,M,L)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    # Метод для отримання списку розмірів у шаблоні
    def get_sizes_list(self):
        return [size.strip() for size in self.available_sizes.split(',')]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class Order(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я покупця")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return f"Замовлення від {self.customer_name}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"