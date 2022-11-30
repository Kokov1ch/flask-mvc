import pandas


def get_reader(conn):
    return pandas.read_sql(
        '''
 SELECT * FROM reader
 ''', conn)

def get_reader_by_name(conn, name):
    cursor = conn.cursor()
    reader = cursor.execute('SELECT reader_name FROM reader WHERE reader_name = ?', (name, ))
    return reader.fetchall()

def get_book_reader(conn, reader_id):
    # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql('''
 WITH get_authors( book_id, authors_name)
 AS(
 SELECT book_id, GROUP_CONCAT(author_name)
 FROM author JOIN book_author USING(author_id)
 GROUP BY book_id
 )
 SELECT title AS Название, authors_name AS Авторы,
 borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
 book_reader_id
 FROM
 reader
 JOIN book_reader USING(reader_id)
 JOIN book USING(book_id)
 JOIN get_authors USING(book_id)
 WHERE reader.reader_id = :id
 ORDER BY 3
 ''', conn, params={"id": reader_id})


# для обработки данных о новом читателе
def get_new_reader(conn, new_reader):
    cur = conn.cursor()
    # добавить нового читателя в базу
    cur.execute('''
 INSERT INTO reader(reader_name) VALUES (:new_reader)
     ''', {"new_reader": new_reader})
    conn.commit()
    return cur.lastrowid


# для обработки данных о взятой книге
def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    cur.executescript(f'''
 INSERT INTO book_reader(book_id, reader_id, borrow_date) VALUES ({book_id},{reader_id}, date('now'));
 UPDATE book
 SET available_numbers = available_numbers - 1
 WHERE book_id = {book_id}
     ''')
    return conn.commit()


def handover_book(conn, reader_book_id):
    cur = conn.cursor()
    cur.executescript(f'''
     UPDATE book
     SET available_numbers = available_numbers + 1
     WHERE book_id = (SELECT book_id FROM book_reader WHERE return_date IS NULL and book_reader_id = {reader_book_id});

     UPDATE book_reader
     SET return_date = DATE()
     WHERE book_reader_id = {reader_book_id}
         ''')

    return conn.commit()
