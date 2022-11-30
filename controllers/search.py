from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_genre, get_author, get_publisher, get_card


@app.route('/search', methods=['get', 'post'])
def search():
    conn = get_db_connection()
    df_author = get_author(conn)
    df_publisher = get_publisher(conn)
    df_genre = get_genre(conn)

    if request.form.get('refresh'):
        genres = []
        publishers =[]
        authors = []
    else:
        genres = [int(item) for item in request.form.getlist('genre_id')]
        publishers = [int(item) for item in request.form.getlist('publisher_id')]
        authors = [int(item) for item in request.form.getlist('author_id')]

    df_card = get_card(conn, publishers, genres, authors)

    html = render_template(
        'search.html',
        authors=df_author,
        publishers=df_publisher,
        genres=df_genre,
        card=df_card,
        sel_authors=authors,
        sel_publishers=publishers,
        sel_genres=genres,
        len=len
    )
    return html
