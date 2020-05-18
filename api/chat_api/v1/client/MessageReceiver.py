import requests
import os
from threading import Thread
import sqlite3
import datetime
import shutil

class MessageReceiver(Thread):
    '''
    Classe che implementa un thread che richiede nuovi messaggi
    interfecciandosi all'API e li salva in un database locale.

    Quindi fa richiesta di nuovi messaggi ogni 5 secondi circa,
    se ci sono nuovi messaggi li inserisce nel database e se ci
    sono dei files manda il path alla coroutine per il download
    che si occuperà di scaricarli.
    '''
    def __init__(self, server_url, user_id, db_path, media_folder):
        Thread.__init__(self)
        self.api_url = server_url
        self.user_id = str(user_id)
        self.db_path = db_path
        self.media_folder = media_folder
        self.query_msg  = 'receive?ID_DEST='
        self.query_file = f'file/{user_id}/'
        self.insert_query = "INSERT INTO 'messages'(id, msg_timestamp, id_mitt, len, type, message) VALUES (?,?,?,?,?,?)"
        self.download_file = self._create_download_file()
        self.stopped = False

    def _create_download_file(self):
        try:
            while True:
                f_path = yield

                url = ''.join([self.api_url, self.query_file, f_path])

                # Richiesta della foto con stream settato a True
                response = requests.get(url=url, stream=True)

                if response.status_code == 200:
                    if not os.path.isdir(self.media_folder):
                        os.makedirs(self.media_folder)
                    
                    out_file = open(os.path.join(self.media_folder, f_path), 'wb')
                    response.raw.decode_content = True
                    
                    shutil.copyfileobj(response.raw, out_file)

                    out_file.close()
        except StopIteration:
            pass
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        
        last_time = datetime.datetime.now()
        now_time  = datetime.datetime.now()

        # Start coroutine
        self.download_file.send(None)

        # Procedura lettura messaggi in arrivo facendo richieste all'api
        while not self.stopped:
            
            now_time = datetime.datetime.now()

            if ( now_time - last_time >= datetime.timedelta(seconds=5) ):
                
                url_req_msg = ''.join([self.api_url,self.query_msg,self.user_id])

                req_msg = requests.get( url=url_req_msg)

                data = req_msg.json()

                status, msg_count, messages = data['status'], data['count'], data['results']

                new_msg_list = []

                for m in messages:

                    # Se file invio path a coroutine per il download
                    if m['type'] == 'file':
                        file_name = m['text'].split('/')[-1]
                        self.download_file.send(file_name)
                        text = file_name
                    else:
                        text = m['text']


                    new_msg_list.append( ( m['id'], m['timestamp'], m['id_mitt'],
                                           m['len'], m['type'], text ))

                conn = sqlite3.connect(self.db_path)
                cur  = conn.cursor()

                cur.executemany(self.insert_query, new_msg_list)

                conn.commit()
                cur.close()
                conn.close()

                last_time = datetime.datetime.now()
