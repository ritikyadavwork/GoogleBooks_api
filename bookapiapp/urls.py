from django.urls import path, include
from .views import search_books
from rest_framework.routers import DefaultRouter
from .views import get_recommendations, submit_recommendation, \
    filter_recommendations, user_interaction

app_name = 'bookapiapp'

urlpatterns = [
    path('search/', search_books, name='search_books'),
    path('recommendations/', get_recommendations, name='get_recommendations'),
    path('recommendations/submit/', submit_recommendation, name='submit_recommendation'),
    path('recommendations/filter/', filter_recommendations, name='filter_recommendations'),
    path('interaction/', user_interaction, name='user_interaction'),

]
