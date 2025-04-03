from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import sys
sys.path.append('C/Users/19/PycharmProjects/pythonproject4/my_project/my_site/star')
from star import views
urlpatterns = [
   path('', views.index, name='star_index'),  # Главная страница
   path('person/<slug:slug>/', views.star_detail, name='star_detail'), # Детальная страница по slug
   path('admin/', admin.site.urls),
   path('', include('star.urls')),
   # Страница «О сайте»
   path('about/', views.about, name='about'),
   # Знаменитости по стране
   path('country/<slug:slug>/', views.stars_by_country, name='stars_by_country'),
   # Знаменитости по виду деятельности
   path('industry/<slug:slug>/', views.stars_by_category, name='stars_by_category'),
   path('add/', views.add_star, name='add_star'),  # Добавление знаменитости
   path('sitemap/', views.sitemap, name='sitemap'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
