from django.urls import path, include
from .views import search_books
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserInteractionViewSet

app_name = 'bookapiapp'

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'interactions', UserInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_books, name='search_books'),

]
