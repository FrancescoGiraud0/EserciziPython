'''
Francesco Giraudo
Classe 5A ROB

HTTP server chat.
'''

from flask import Flask, jsonify, request, send_file, make_response
from werkzeug.utils import secure_filename
import sqlite3 as sqlite
import datetime
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = './media/'

@app.route('/api/v1/user_list', methods=['GET', 'POST'])
def get_users_list():
    """
    Metodo per l'invio di tutti gli utenti salvati nel db in formato JSON.

    Il client farà una richiesta HTTP di tipo get con il seguente formato:

    http://IP_SERVER:PORTA/api/v1/user_list

    Riceverà quindi come risposta un JSON con il seguente formato:
    
    {
      datetime : %Y-%m-%d %H:%M:%S,
      status : XXX,
      description : XXX,
      elaboration_time : XXX,
      count: XXX,
      results: [
                    {
                        id : XXX,
                        name : XXX,
                        surname : XXX,
                    }
               ]
    }
    """

    start_time = datetime.datetime.now()

    answer = {  'datetime' : None,
                'status' : None,
                'description' : None,
                'elaboration_time' : 0.0,
                'count' : None,
                'results' : []
             }

    try:
        conn = sqlite.connect('./db/chat_schema.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id, nome, cognome FROM users')

        results = convert_users_to_dict(cursor.fetchall())

        answer['count'] = len(results)
        answer['results'] = results

        cursor.close()
        conn.close()

        answer['status'] =  'OK'
        answer['description'] = 'Received all users information.'

        end_time = datetime.datetime.now()
        delta = end_time - start_time

        answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        answer['elaboration_time'] = delta.total_seconds()
    except:
        cursor.close()
        conn.close()

        answer['status'] = 'DB ERROR'
        answer['description'] = 'Error: Error with the database.'

        end_time = datetime.datetime.now()
        delta = end_time - start_time

        answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        answer['elaboration_time'] = delta.total_seconds()

    return jsonify(answer)


@app.route('/api/v1/send', methods=['GET', 'POST'])
def send_msg():
    '''
    Metodo per l'invio dei messaggi.
    Il mittente farà una richiesta HTTP GET o POST al server con una query string avente
    il formato:
    
    http://IP_SERVER:PORTA/api/v1/send?ID_DEST=XXX&ID_MITT=XXX&text=XXX

    Nel body POST è possibile inserire il file, in questo caso il campo text della query
    string non sarà obbligatorio, ma verrà salvato il nome del file con il seguente formato
    nel campo "message" del database:

    ID_MITT_ID_DEST_[NOMEFILE+ESTENSIONE]

    I files vengono salvati nella cartella media avente la seguente struttura di
    sottocartelle:
    
    +---- chat_api
        |
        +---- v1
            |
            +---- server
                |
                +---- media
                    |
                    +--- XXX -> (XXX = id utente del mittente)

    Quindi, se non verificano errori, verrà restituito un json il seguente formato:

    {
      datetime : XXX,
      status : XXX,
      description : XXX,
      elaboration_time : XXX
    }
    '''

    start_time = datetime.datetime.now()

    answer = {  'datetime' : None,
                'status' : None,
                'file_loc' : None,
                'description' : None,
                'elaboration_time' : 0.0 }

    args_list = ['ID_DEST', 'ID_MITT']
    
    # Verifica se ci sono tutti i parametri necessari nella query string
    if all((True if arg in request.args else False) for arg in args_list):
        
        try:
            id_dest = int(request.args['ID_DEST'])
            id_mitt = int(request.args['ID_MITT'])
        except ValueError:
            answer['status'] = 'ID Error'
            answer['description'] = 'Error: ID_DEST and ID_MITT must be integers.'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

            return jsonify(answer)
        
        try:
            text = request.args['text'] if 'text' in request.args else ''
            if (len(text)>250 or len(text)<=0) and request.method=='GET':
                # Errore se non definito text e non caricato file
                answer['status'] =  'Length Error'
                answer['description'] = 'Error: Text message is too long or not defined.'

                end_time = datetime.datetime.now()
                delta = end_time - start_time

                answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
                answer['elaboration_time'] = delta.total_seconds()

                return jsonify(answer)
        except:
            answer['status'] =  'Message Error'
            answer['description'] = 'Error: Error with text message.'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

            return jsonify(answer)

        try:
            timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')
        except:
            answer['status'] =  'Timestamp Error'
            answer['description'] = 'Error: Incorrect timestamp format (it must be %Y-%m-%d %H:%M:%S).'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

            return jsonify(answer)

        # Gestione salvataggio files
        try:
            if request.method == 'POST':
                msg_type = 'file'

                f = request.files['file']

                file_name = f.filename.split('/')[-1]

                file_name = secure_filename(f'{id_mitt}_{id_dest}_{secure_filename(file_name)}')
                file_dir = os.path.join(str(app.config['UPLOAD_FOLDER']), str(id_mitt))

                if not os.path.isdir(file_dir):
                    os.makedirs(file_dir)
                
                text = os.path.join(file_dir, file_name)

                f.save(text)

                answer['file_loc'] = text

            elif request.method == 'GET':
                msg_type = 'text'

            elif request.method == 'GET':
                msg_type = 'text'

        except:
            answer['status'] =  'Request Error'
            answer['description'] = 'Error: Incorrect HTTP POST request.'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

            return jsonify(answer)


        # Salvataggio messaggio nel database
        try:
            query = f''' INSERT INTO messages(msg_timestamp, id_dest, id_mitt, message, len, type) VALUES (
                        '{timestamp}', 
                        {id_dest}, 
                        {id_mitt}, 
                        '{text}', 
                        {len(text)},
                        '{msg_type}' );'''

            conn = sqlite.connect('./db/chat_schema.db')
            cursor = conn.cursor()

            cursor.execute(query)

            conn.commit()

            cursor.close()
            conn.close()

        except:
            cursor.close()
            conn.close()

            answer['status'] =  'Database Error'
            answer['description'] = 'Error: Error with database.'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

            return jsonify(answer)

        answer['status'] =  'OK'
        answer['description'] = 'Message sent successfully.'

        end_time = datetime.datetime.now()
        delta = end_time - start_time

        answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        answer['elaboration_time'] = delta.total_seconds()

    else:
        answer['status'] = 'Query String Error'
        answer['description'] = '''Error: Not provided all arguments in query (expected .../send?ID_DEST=XXX&ID_MITT=XXX&text=XXX&time=XXX)'''

        end_time = datetime.datetime.now()
        delta = end_time - start_time

        answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        answer['elaboration_time'] = delta.total_seconds()

    return jsonify(answer)

@app.route('/api/v1/receive', methods=['GET', 'POST'])
def receive_msg():
    '''
    Metodo per la ricezione dei messaggi.
    Il destinatario farà una richiesta HTTP GET al seguente URL:
    
    http://IP_SERVER:PORTA/api/v1/receive?ID_DEST=XXX

    con questi parametri facoltativi:
        - ID_MITT
        - date_from, date_to
        - size

    Quindi verrà restituito un json il seguente formato:
    { 
      datetime : %Y-%m-%d %H:%M:%S,
      status : XXX,
      description : XXX,
      elaboration_time : XXX,
      count: XXX,
      date_from : %Y-%m-%d %H:%M:%S,  -> Data del msg più vecchio (if no results is null)
      date_to : %Y-%m-%d %H:%M:%S, -> Data del msg più recente (if no results is null)
      results: [
                    { 
                        id : XXX,
                        timestamp : %Y-%m-%d %H:%M:%S,
                        id_mitt : XXX,
                        name_mitt : XXX,
                        surname_mitt : XXX,
                        len : XXX,
                        text : XXX,
                        type : XXX
                    }
               ]
    }
    '''

    start_time = datetime.datetime.now()

    answer = {  'datetime' : None,
                'status' : None,
                'description' : None,
                'elaboration_time' : 0.0,
                'count' : 0,
                'date_from' : None,
                'date_to' : None,
                'results' : [] }
    
    try:
        id_dest = int(request.args['ID_DEST'])
        id_mitt = None
        id_list = [id_dest]

        if 'ID_MITT' in request.args:
            id_mitt = int(request.args['ID_MITT'])
            id_list.append(id_mitt)
        
    except ValueError:
        answer['status'] = 'ID Error'
        answer['description'] = 'Error: IDs must be integers.'

        end_time = datetime.datetime.now()
        delta = end_time - start_time

        answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        answer['elaboration_time'] = delta.total_seconds()

        return jsonify(answer)
    
    date_from, date_to, size = None, None, None

    if 'date_from' in request.args:
        date_from = request.args['date_from']
        if 'date_to' in request.args:
            date_to = request.args['date_to']
    
    if 'size' in request.args:
        try:
            size = int(request.args['size'])
        except ValueError:
            answer['status'] = 'Size ERROR'
            answer['description'] = 'Error: size must be an integer.'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

            return jsonify(answer)

    if exist(id_list):
        results = []
        try:
            results = req_messages(id_dest, id_mitt=id_mitt,date_from=date_from, date_to=date_to, size=size)

            answer['count'] = len(results)
            answer['date_from'] = results[-1]['timestamp'] if answer['count']>0 else None
            answer['date_to'] = results[0]['timestamp'] if answer['count']>0 else None
            answer['results'] = results

            answer['status'] = 'OK'
            answer['description'] = 'Messages received successfully.'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

        except:
            answer['status'] = 'DB ERROR'
            answer['description'] = 'Error: Error with the database or wrong query.'

            end_time = datetime.datetime.now()
            delta = end_time - start_time

            answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            answer['elaboration_time'] = delta.total_seconds()

    else:
        answer['status'] = 'ID Not Exist ERROR'
        answer['description'] = 'Error: ID_DEST or ID_MITT does not exist.'

        end_time = datetime.datetime.now()
        delta = end_time - start_time

        answer['datetime'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        answer['elaboration_time'] = delta.total_seconds()

    return jsonify(answer)

@app.route('/api/v1/file/<id>/<file_name>')
def request_file(id, file_name):

    path = os.path.join(app.config['UPLOAD_FOLDER'], id, file_name)

    if os.path.isfile(path):
        return send_file(path)
    else:
        return make_response( jsonify({'description' : 'File not found'}), 404)

def req_messages(id_dest, id_mitt=None, date_from=None, date_to=None, size=None):
    conn = sqlite.connect('./db/chat_schema.db')
    cursor = conn.cursor()

    query = f'''
SELECT m.id, m.msg_timestamp, m.id_mitt, u.nome, u.cognome, m.len, m.message, m.type
FROM users AS u INNER JOIN messages as m ON u.id=m.id_dest
WHERE m.id_dest = {id_dest}\n AND received = 0\n'''

    if id_mitt != None:
        query += f' AND m.id_mitt={id_mitt}\n'
    
    if date_from != None:
        if date_to != None:
            query += f" AND m.msg_timestamp BETWEEN DATETIME('{date_from}') AND DATETIME('{date_to}')\n"
        else:
            query += f" AND m.msg_timestamp >= DATETIME('{date_from}')\n"


    query += 'ORDER BY m.msg_timestamp DESC\n' 

    if size != None:
        query += f'LIMIT {size}'

    query += ';'

    cursor.execute(query)

    results = convert_messages_to_dict(cursor.fetchall())

    query_list = query.split('\n')[:-1]
    
    query_list[0] = 'UPDATE messages SET received = 1 WHERE id IN ('
    query_list[1] = 'SELECT m.id'
    query_list.append(');')

    update_query = '\n'.join(query_list)
    
    cursor.execute(update_query)

    conn.commit()

    cursor.close()
    conn.close()

    return results

def convert_messages_to_dict(messages):
    msg_list = [
                {'id' : m[0],
                 'timestamp' : m[1],
                 'id_mitt' : m[2],
                 'name_mitt' : m[3],
                 'surname_mitt' : m[4],
                 'len' : m[5],
                 'text' : m[6],
                 'type' : m[7] }
               for m in messages ]
    
    return msg_list

def convert_users_to_dict(users):
    users_list = [
                {'id' : u[0],
                 'name' : u[1],
                 'surname' : u[2],}
               for u in users ]
    
    return users_list

def exist(users):
    '''
        Function that take in input an id_user or a list of id_user
        and return True if they are in users database.
    '''

    if type(users) != list:
        users = [users]
    
    res = True

    try:
        conn = sqlite.connect('./db/chat_schema.db')
        cursor = conn.cursor()
        
        for u in users:
            query = f'SELECT COUNT(*) FROM users WHERE id = {u}'
            cursor.execute(query)

            r = cursor.fetchone()[0]
            
            res = r==1

            if not res:
                break
        
        cursor.close()
        conn.close()

    except:
        res = False
    
    return res

# Creazione della cartella per il salvataggio dei file se non esistente
if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.run()
