import requests
from django.http import JsonResponse


def fetch_books_api(query=None, author=None, category=None):
    if not query:
        return {'error': 'No query parameter provided'}

    api_url = 'https://www.googleapis.com/books/v1/volumes'

    search_query = ''

    if query:
        search_query += query
    if author:
        if search_query:
            search_query += '+'
        search_query += f'inauthor:{author}'
    if category:
        if search_query:
            search_query += '+'
        search_query += f'subject:{category}'

    params = {
        'q': query,
        'key': 'AIzaSyAdScHOuR0EWiwYvzib7VCQ738zw3cl54I'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.HTTPError as http_err:
        return {'error': f'HTTP error occurred: {http_err}'}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': f'Connection error occurred: {conn_err}'}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': f'Timeout error occurred: {timeout_err}'}
    except requests.exceptions.RequestException as req_err:
        return {'error': f'Request error occurred: {req_err}'}

    if response.status_code == 200:
        data = response.json()
        if 'items' not in data:
            return {'error': 'No books found'}
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
