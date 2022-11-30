from app import app
from flask import render_template, request, session
# import sqlite3
from utils import get_db_connection
from models.index_model import get_reader, get_book_reader, get_new_reader, borrow_book, handover_book, get_reader_by_name


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()
    tmp = ""
    # нажата кнопка Найти
    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id
    else:
        session['reader_id'] = 1
    if request.values.get('new_reader'):
        array = get_reader_by_name(conn, request.values.get('new_reader'))
        for row in array:
            tmp = row[0]
    # нажата кнопка Добавить со страницы Новый читатель
    # (взять в комментарии, пока не реализована страница Новый читатель)
    if (request.values.get('new_reader')) and (request.values.get('new_reader') != tmp):
        #print(request.values.get('new_reader'))
        print(get_reader_by_name(conn, request.values.get('new_reader')))
        session['reader_id'] = get_new_reader(conn, request.values.get('new_reader'))
    # нажата кнопка Взять со страницы Поиск
    # (взять в комментарии, пока не реализована страница Поиск)
    if request.values.get('book'):
        book_id = int(request.values.get('book'))
        borrow_book(conn, book_id, session['reader_id'])
    # нажата кнопка Не брать книгу со страницы Поиск
    if request.values.get('noselect'):
        a = 1
    # вошли первый раз
    if request.values.get('handover'):
        handover_book(conn, request.values.get('handover'))
    if request.values.get('book'):
        borrow_book(conn,int(request.values.get('book')), session['reader_id'])
    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    # выводим форму
    html = render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_reader,
        book_reader=df_book_reader,
        len=len
    )
    return html