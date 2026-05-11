from django import forms
from .models import ProductRating


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        label="Ваше ім'я",
        widget=forms.TextInput(attrs={
            "placeholder": "Наприклад: Антон",
            "class": "form-input"
        })
    )

    phone = forms.CharField(
        max_length=20,
        label="Телефон",
        widget=forms.TextInput(attrs={
            "placeholder": "+380...",
            "class": "form-input"
        })
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "example@gmail.com",
            "class": "form-input"
        })
    )

    address = forms.CharField(
        max_length=255,
        label="Адреса доставки",
        widget=forms.TextInput(attrs={
            "placeholder": "Місто, відділення Нової пошти / адреса",
            "class": "form-input"
        })
    )


class NewsletterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Ваше ім'я",
            "class": "newsletter-input"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Ваш email",
            "class": "newsletter-input"
        })
    )


class RatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ["customer_name", "score"]

        widgets = {
            "customer_name": forms.TextInput(attrs={
                "placeholder": "Ваше ім'я",
                "class": "form-input"
            }),
            "score": forms.RadioSelect(choices=[
                (1, "1"),
                (2, "2"),
                (3, "3"),
                (4, "4"),
                (5, "5"),
            ])
        }