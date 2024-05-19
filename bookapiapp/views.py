import requests
from django.http import JsonResponse
from django.shortcuts import render
from .api import fetch_books_api
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, UserInteraction
from .serializers import BookSerializer, UserInteractionSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


def search_books(request):
    query = request.GET.get('q', 'coding')
    author = request.GET.get('author')
    category = request.GET.get('category')

    books = fetch_books_api(query=query, author=author, category=category)

    if 'error' in books:
        return JsonResponse(books, status=400)

    return render(request, 'search.html', {'books': books, 'query': query})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        book = self.get_object()
        user = request.user
        interaction, created = UserInteraction.objects.get_or_create(book=book, user=user)
        interaction.liked = True
        interaction.save()
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        book = self.get_object()
        user = request.user  # Assuming user is authenticated
        UserInteraction.objects.filter(book=book, user=user).delete()
        return Response({'status': 'unliked'})


class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['genre', 'rating', 'publication_date']
    ordering_fields = ['title', 'rating', 'publication_date']
