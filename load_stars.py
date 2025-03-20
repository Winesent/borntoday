import os
import django
import datetime
import re

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'borntoday.settings')
django.setup()

# Импортируем модели после настройки Django
from star.models import Star, Country, Category

# Словарь для преобразования русских названий месяцев в числа
MONTHS = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
    'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
}


# Функция для преобразования даты вида "11 ноября 1974" в объект date
def parse_russian_date(date_str):
    # Разбиваем строку на компоненты
    match = re.match(r'(\d+) (\w+) (\d+)', date_str)
    if not match:
        raise ValueError(f"Неверный формат даты: {date_str}")

    day, month_name, year = match.groups()
    # Преобразуем месяц в число
    month_num = MONTHS.get(month_name.lower())
    if not month_num:
        raise ValueError(f"Неизвестный месяц: {month_name}")

    # Создаем объект date
    return datetime.date(int(year), month_num, int(day))


# Исходные данные
stars_data = [
    {"id": 1, "name": "Леонардо ДиКаприо", "country": "США", "category": "Кино", "birth_date": "11 ноября 1974",
     "content": "Американский актер и продюсер, обладатель премии Оскар.", "is_published": True},

    {"id": 2, "name": "Адель", "country": "Великобритания", "category": "Музыка", "birth_date": "5 мая 1988",
     "content": "Британская певица и автор песен, лауреат Грэмми.", "is_published": True},

    {"id": 3, "name": "Криштиану Роналду", "country": "Португалия", "category": "Спорт", "birth_date": "5 февраля 1985",
     "content": "Португальский футболист, один из лучших нападающих мира.", "is_published": True},

    {"id": 4, "name": "Том Хэнкс", "country": "США", "category": "Кино", "birth_date": "9 июля 1956",
     "content": "Американский актер, дважды обладатель премии Оскар.", "is_published": True},

    {"id": 5, "name": "Бейонсе", "country": "США", "category": "Музыка", "birth_date": "4 сентября 1981",
     "content": "Американская певица, актриса и продюсер, лидер группы Destiny's Child.", "is_published": True},

    {"id": 6, "name": "Элтон Джон", "country": "Великобритания", "category": "Музыка", "birth_date": "25 марта 1947",
     "content": "Британский певец, композитор и пианист.", "is_published": True},

    {"id": 7, "name": "Анжелина Джоли", "country": "США", "category": "Кино", "birth_date": "4 июня 1975",
     "content": "Американская актриса, режиссер и гуманитарный деятель.", "is_published": True},

    {"id": 8, "name": "Уилл Смит", "country": "США", "category": "Кино", "birth_date": "25 сентября 1968",
     "content": "Американский актер, продюсер и музыкант, обладатель премии Оскар.", "is_published": True},

    {"id": 9, "name": "Рианна", "country": "Барбадос", "category": "Музыка", "birth_date": "20 февраля 1988",
     "content": "Барбадосская певица, актриса и предпринимательница.", "is_published": True},

    {"id": 10, "name": "Дэвид Бекхэм", "country": "Великобритания", "category": "Спорт", "birth_date": "2 мая 1975",
     "content": "Бывший английский футболист, игравший за Манчестер Юнайтед и Реал Мадрид.", "is_published": True}
]


def load_stars():
    # Создаем словари для хранения объектов стран и категорий
    countries = {}
    categories = {}

    print("Начало загрузки данных...")

    # Создаем страны, если они не существуют
    for star_data in stars_data:
        country_name = star_data["country"]
        if country_name not in countries:
            country, created = Country.objects.get_or_create(name=country_name)
            countries[country_name] = country
            if created:
                print(f"Создана страна: {country_name}")

    # Создаем категории, если они не существуют
    for star_data in stars_data:
        category_name = star_data["category"]
        if category_name not in categories:
            category, created = Category.objects.get_or_create(title=category_name)
            categories[category_name] = category
            if created:
                print(f"Создана категория: {category_name}")

    # Создаем знаменитостей
    for star_data in stars_data:
        # Проверяем, существует ли уже такая знаменитость
        if not Star.objects.filter(name=star_data["name"]).exists():
            try:
                # Используем нашу функцию для преобразования русской даты
                birth_date = parse_russian_date(star_data["birth_date"])

                # Создаем знаменитость
                star = Star(
                    name=star_data["name"],
                    country=countries[star_data["country"]],
                    birth_date=birth_date,
                    content=star_data["content"],
                    is_published=True
                )
                star.save()  # Сохраняем, чтобы создать slug

                # Добавляем категорию
                star.categories.add(categories[star_data["category"]])

                print(f"Создана знаменитость: {star.name}")
            except Exception as e:
                print(f"Ошибка при создании знаменитости {star_data['name']}: {e}")
        else:
            print(f"Знаменитость {star_data['name']} уже существует, пропускаем")

    print("Загрузка данных завершена.")


if __name__ == "__main__":
    load_stars()
