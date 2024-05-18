import requests
from django.http import JsonResponse


def fetch_books_api(query):
    if not query:
        return {'error': 'No query parameter provided'}

    api_url = 'https://www.googleapis.com/books/v1/volumes'

    params = {
        'q': query,
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
