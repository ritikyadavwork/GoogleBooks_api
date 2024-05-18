import requests
from django.http import JsonResponse
from django.shortcuts import render
from .api import fetch_books_api


def search_books(request):
    query = request.GET.get('q', 'coding')
    books = fetch_books_api(query)

    if 'error' in books:
        return JsonResponse(books, status=400)

    return render(request, 'search.html', {'books': books, 'query': query})

