import requests

def parse_books(data):
    books = []
    for doc in data.get('docs', []):
        book = {
            'title': doc.get('title'),
            'authors': doc.get('author_name', []),
            'year': doc.get('first_publish_year'),
            'cover_image': f"http://covers.openlibrary.org/b/id/{doc.get('cover_i')}-L.jpg" if doc.get('cover_i') else None,
            'source': 'openlibrary',
            'download_links': {
                'read': f"https://openlibrary.org{doc.get('key')}" if doc.get('key') else None,
                'detail': f"https://openlibrary.org{doc.get('key')}" if doc.get('key') else None,
            }
        }
        books.append(book)
    return books

def fetch_book_details(book_id):
    api_url = f"https://openlibrary.org/works/{book_id}.json"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_books_from_api(query, page=1):
    api_url = f"https://openlibrary.org/search.json?q={query}&page={page}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        books = parse_books(data)
        return books
    else:
        return None