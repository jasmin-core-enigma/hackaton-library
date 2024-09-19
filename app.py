# app.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    author = request.form['author']
    books = get_books_by_author(author)
    results = []
    for book in books:
        title = book['volumeInfo']['title']
        published_date = book['volumeInfo'].get('publishedDate', 'N/A')
        movie_info = get_movie_adaptation(title)
        results.append({
            'title': title,
            'published_date': published_date,
            'movie_info': movie_info
        })
    return render_template('results.html', results=results)

def get_books_by_author(author):
    url = f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}'
    response = requests.get(url)
    return response.json().get('items', [])

def get_movie_adaptation(title):
    url = f'http://www.omdbapi.com/?t={title}&apikey=YOUR_OMDB_API_KEY'
    response = requests.get(url)
    data = response.json()
    if data['Response'] == 'True':
        return {
            'title': data['Title'],
            'year': data['Year']
        }
    return None

if __name__ == '__main__':
    app.run(debug=True)