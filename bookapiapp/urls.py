from django.contrib import admin
from django.urls import path, include
from .views import search_books

app_name = 'bookapiapp'

urlpatterns = [
    path('search/', search_books, name='search_books'),

]
