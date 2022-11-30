from app import app
from flask import render_template


@app.route('/book', methods=['get'])
def book():
    html = render_template(
        'book.html',
    )
    return html