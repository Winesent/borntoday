from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.contrib import messages
from datetime import date, timedelta
from .models import Star, Country, Category
from .forms import StarForm


def index(request):
    """
    Главная страница: выводим все звёзды + выделяем, у кого сегодня/завтра/послезавтра день рождения.
    """
    # Получаем все опубликованные звезды
    all_stars = Star.objects.filter(is_published=True)

    # Получаем текущую дату
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    # Находим звезд с днями рождения
    today_stars = []
    tomorrow_stars = []
    day_after_tomorrow_stars = []

    for star in all_stars:
        # Проверяем месяц и день (без учета года)
        if star.birth_date.month == today.month and star.birth_date.day == today.day:
            today_stars.append(star)
        elif star.birth_date.month == tomorrow.month and star.birth_date.day == tomorrow.day:
            tomorrow_stars.append(star)
        elif star.birth_date.month == day_after_tomorrow.month and star.birth_date.day == day_after_tomorrow.day:
            day_after_tomorrow_stars.append(star)

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': all_stars,
        'today_stars': today_stars,
        'tomorrow_stars': tomorrow_stars,
        'day_after_tomorrow_stars': day_after_tomorrow_stars,
        'today_date': today,
        'tomorrow_date': tomorrow,
        'day_after_tomorrow_date': day_after_tomorrow,
        'star_countries': countries,
        'star_categories': categories,
        'title': 'Дни рождения звезд'
    }
    return render(request, 'star/index.html', context)


def star_detail(request, slug):
    """
    Детальная страница конкретной звезды: /person/<slug>/
    """
    # Получаем объект звезды по slug или выбрасываем 404 ошибку
    star = get_object_or_404(Star, slug=slug, is_published=True)

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'star': star,
        'star_countries': countries,
        'star_categories': categories,
    }

    return render(request, 'star/star-detail.html', context)


def about(request):
    """
    Страница «О сайте».
    """
    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'title': 'О сайте',
        'description': 'Сайт создан в учебных целях. Данные сгенерированы нейросетью.',
        'star_countries': countries,
        'star_categories': categories,
    }
    return render(request, 'star/about.html', context)


def stars_by_country(request, slug):
    country = get_object_or_404(Country, slug=slug)
    filtered_stars = Star.objects.filter(country=country, is_published=True)

    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': filtered_stars,
        'country_name': country.name,
        'star_countries': countries,
        'star_categories': categories,
        'title_template': 'Знаменитости из страны'
    }
    return render(request, 'star/country.html', context)


def stars_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    filtered_stars = Star.objects.filter(categories=category, is_published=True)

    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': filtered_stars,
        'category_name': category.title,
        'star_countries': countries,
        'star_categories': categories,
        'title_template': 'Знаменитости из отрасли',
    }
    return render(request, 'star/industry.html', context)


def add_star(request):
    """
    Представление для добавления новой знаменитости
    """
    if request.method == 'POST':
        form = StarForm(request.POST, request.FILES)
        if form.is_valid():
            star = form.save(commit=False)
            star.is_published = True
            star.save()
            form.save_m2m()  # Сохраняем связи many-to-many
            messages.success(request, f'Знаменитость "{star.name}" успешно добавлена!')
            return redirect('star_detail', slug=star.slug)
    else:
        form = StarForm()

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'form': form,
        'title': 'Добавление знаменитости',
        'star_countries': countries,
        'star_categories': categories,
    }
    return render(request, 'star/add-star.html', context)


def sitemap(request):
    """Карта сайта со списком всех знаменитостей и алфавитным указателем"""
    # Получаем все опубликованные звезды, сортированные по имени
    stars = Star.objects.filter(is_published=True).order_by('name')

    # Русский алфавит (включая Ё)
    russian_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    english_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Определяем, какие буквы есть в базе
    available_letters = set()

    # Для русского алфавита
    for letter in russian_alphabet:
        if Star.objects.filter(is_published=True, name__istartswith=letter).exists():
            available_letters.add(letter)

    # Для английского алфавита
    for letter in english_alphabet:
        if Star.objects.filter(is_published=True, name__istartswith=letter).exists():
            available_letters.add(letter)

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': stars,
        'russian_alphabet': russian_alphabet,
        'english_alphabet': english_alphabet,
        'available_letters': available_letters,
        'star_countries': countries,
        'star_categories': categories,
        'title': 'Карта сайта - Все знаменитости',
    }
    return render(request, 'star/sitemap.html', context)


def sitemap_letter(request, letter):
    """Карта сайта с фильтрацией по первой букве имени"""
    # Приводим букву к верхнему регистру
    letter = letter.upper()

    # Фильтруем звезды по первой букве имени
    stars = Star.objects.filter(
        is_published=True,
        name__istartswith=letter
    ).order_by('name')

    # Русский и английский алфавиты
    russian_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    english_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Определяем, какие буквы есть в базе
    available_letters = set()
    for l in russian_alphabet + english_alphabet:
        if Star.objects.filter(is_published=True, name__istartswith=l).exists():
            available_letters.add(l)

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': stars,
        'current_letter': letter,
        'russian_alphabet': russian_alphabet,
        'english_alphabet': english_alphabet,
        'available_letters': available_letters,
        'star_countries': countries,
        'star_categories': categories,
        'title': f'Карта сайта - Знаменитости на букву {letter}',
    }
    return render(request, 'star/sitemap_letter.html', context)