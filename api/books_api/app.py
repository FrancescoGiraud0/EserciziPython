from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['DEBUG'] = True

books = [
    {
    'id' : 1,
    'title' : 'Storia della tua vita',
    'author' : 'Ted Chiang',
    'year_published' : 2002
    },
    {
    'id': 2,
    'title':'Respiro',
    'author':'Ted Chiang',
    'year_published': 2019
    },
    {
    'id': 3,
    'title' : 'Antifragile',
    'author' : 'Nassim Nicholas Taleb',
    'year_published' : 2019 
    },
    {
    'id': 4,
    'title' : 'Social Physics',
    'author' : 'Alex Pentland',
    'year_published' : 2014
    },
    {
    'id': 5,
    'title' : 'The Black Box Society',
    'author' : 'Frank Pasquale',
    'year_published' : 2015
    },
]

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    if 'id' in request.args:
        try:
            id = int(request.args['id'])
        except ValueError:
            return 'Error: id field must be integer.'
    else:
        return 'Error: No id field provided. Please retry adding the id field.'
    
    result = []

    for book in books:
        if book['id'] == id:
            result.append(book)

    return jsonify(result)

@app.route('/api/v1/resources/books/author', methods=['GET'])
def api_author():
    if 'author' in request.args:
        author = request.args['author']
    else:
        return 'Error: No author field provided. Please retry adding the author field.'
    
    result = []

    for book in books:
        if author.lower() in book['author'].lower():
            result.append(book)

    return jsonify(result)

app.run()