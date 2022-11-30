import pandas as pd

def to_string(list):
    s = [str(i) for i in list]
    res = ",".join(s)

    return res
def get_publisher(conn):
    return pd.read_sql('''
        SELECT publisher_id, publisher_name, COUNT(book.book_id)
        FROM publisher
        JOIN book USING(publisher_id)
        GROUP BY publisher_name''', conn)


def get_genre(conn):
    return pd.read_sql('''
        SELECT genre_id, genre_name, COUNT(book.book_id)
        FROM genre
        JOIN book USING(genre_id)
        GROUP BY genre_name''', conn)


def get_author(conn):
    return pd.read_sql('''
        SELECT author_id, author_name, COUNT(book.book_id)
        FROM author
        JOIN book_author USING(author_id)
        JOIN book USING(book_id)
        GROUP BY author_name''', conn)


def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]

    # Join list items using join()
    res = ",".join(s)

    return res

def get_card(conn, publishers, genres, authors):
    publishers = to_string(publishers)
    authors = to_string(authors)
    genres = to_string(genres)
    return pd.read_sql(f'''
        SELECT
        	title AS 'Название',
        	group_concat(DISTINCT author_name) AS 'Авторы',
        	genre_name AS 'Жанр',
        	publisher_name AS 'Издательство',
            year_publication AS 'Год_издания',
            available_numbers AS 'Количество',
            book_id AS 'ID'
        FROM book
        JOIN genre USING(genre_id)
        JOIN publisher USING(publisher_id)
        JOIN book_author USING(book_id)
        JOIN author USING(author_id)
        GROUP BY book_id
        HAVING (genre_id IN ({genres}) OR ({not genres}))
            AND (publisher_id IN ({publishers}) OR ({not publishers}))
            AND (author_id IN ({authors}) OR ({not authors}))
        ORDER BY
            title,
            available_numbers DESC,
            genre_name,
            year_publication DESC 
    ''', conn)
