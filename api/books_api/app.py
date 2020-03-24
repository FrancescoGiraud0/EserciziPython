from flask import Flask, jsonify, request
import sqlite3 as sqlite

app = Flask(__name__)
app.config['DEBUG'] = True

def convert_to_dict(books):
    result = [
        {
            'id': int(b[0]),
            'title': b[1],
            'author': b[2],
            'year_published': int(b[3])
        }
        for b in books ]

    return result

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite.connect('./db/books.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Books;')
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    result = convert_to_dict(books)

    return jsonify(result)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    if 'id' in request.args:
        try:
            id = int(request.args['id'])
        except ValueError:
            return 'Error: id field must be integer.'
    else:
        return 'Error: No id field provided. Please retry adding the id field.'
    
    conn = sqlite.connect('./db/books.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM Books WHERE id = {id};')
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    result = convert_to_dict(books)

    return jsonify(result)

@app.route('/api/v1/resources/books/author', methods=['GET'])
def api_author():
    if 'author' in request.args:
        author = request.args['author']
    else:
        return 'Error: No author field provided. Please retry adding the author field.'

    conn = sqlite.connect('./db/books.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM Books WHERE lower(author) LIKE "%{author.lower()}%";')
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    result = convert_to_dict(books)

    return jsonify(result)

app.run()