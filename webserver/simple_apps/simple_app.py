from flask import Flask

app = Flask(__name__)

@app.route('/') # Decoratore
def index():
    return 'Ciao!'

@app.route('/pagina/')
def index2():
    return 'Ciao da pagina!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')