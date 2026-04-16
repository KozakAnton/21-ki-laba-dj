from django.shortcuts import render

def index(request):
    context = {
        'title': 'Головна сторінка проекту',
        'content': 'Вітаємо! Тут ви знайдете посилання на всі лабораторні роботи.'
    }
    return render(request, 'labs/index.html', context)

def about(request):
    context = {
        'title': 'Про Лабу 1',
        'content': 'Ця сторінка демонструє використання контексту в Django.'
    }
    return render(request, 'labs/about.html', context)