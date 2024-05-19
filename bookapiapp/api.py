import requests
from django.http import JsonResponse


def fetch_books_api(keyword, author, category):
    api_url = 'https://www.googleapis.com/books/v1/volumes'

    search_query = ''

    if keyword:
        search_query += keyword
    if author:
        if search_query:
            search_query += '+'
        search_query += f'inauthor:{author}'
    if category:
        if search_query:
            search_query += '+'
        search_query += f'subject:{category}'

    params = {
        'q': search_query,
        'key': 'AIzaSyAdScHOuR0EWiwYvzib7VCQ738zw3cl54I'
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()

        books = [
            {
                'title': item['volumeInfo'].get('title'),
                'authors': item['volumeInfo'].get('authors'),
                'description': item['volumeInfo'].get('description'),
                'cover_image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
                'ratings_count': item['volumeInfo'].get('ratingsCount'),
                'average_rating': item['volumeInfo'].get('averageRating')
            }
            for item in data.get('items', [])
        ]
        return books
    else:
        return {'error': 'Failed to fetch data from Google Books API'}
