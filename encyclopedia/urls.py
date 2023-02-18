from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:title>', views.article, name='article'),
    path('search/', views.search, name='search'),
    path('create/', views.create_article, name='create'),
    path('edit/<str:title>', views.edit_article, name='edit'),
    path('random/', views.random_article, name='random'),
    path('404/', views.custom_not_found_view, name='404'),
]

