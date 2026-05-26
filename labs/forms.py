from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, password_validation

from .models import ProductRating


User = get_user_model()


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Логін",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Придумайте логін"
        })
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-input",
            "placeholder": "example@gmail.com"
        })
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Введіть пароль"
        })
    )

    password2 = forms.CharField(
        label="Повторіть пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Повторіть пароль"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує.")

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логін",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Ваш логін"
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Ваш пароль"
        })
    )


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


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-input",
            "placeholder": "Введіть email вашого акаунта"
        })
    )


class PasswordResetConfirmForm(forms.Form):
    code = forms.CharField(
        label="Код з email",
        max_length=6,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "6-значний код"
        })
    )

    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Новий пароль"
        })
    )

    new_password2 = forms.CharField(
        label="Повторіть новий пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Повторіть новий пароль"
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають.")

        if password1:
            password_validation.validate_password(password1)

        return cleaned_data