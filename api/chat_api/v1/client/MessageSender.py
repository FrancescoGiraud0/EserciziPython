import requests
import os
from threading import Thread

class MessageSender(Thread):
    '''
    Classe che implementa un thread che richiede in input
    un messaggio come stringa.
    
    Se la stringa contiene /file come prima parola, quello
    che segue indica il percorso ad un file da inviare come
    messaggio.
    '''
    def __init__(self, api_url, user_id, id_dest):
        Thread.__init__(self)
        self.api_url = api_url
        self.user_id = str(id_dest)
        self.id_dest = str(user_id)
        self.api_method  = 'send'
    
    def send_file(self, path):

        if os.path.isfile(path):

            f = open(path, 'rb')

            files = {'file' : f}

            url = self.api_url+self.api_method+f'?ID_DEST={self.id_dest}&ID_MITT={self.user_id}'
        
            response = requests.post(url=url, files=files)

            f.close()

            res_json = response.json()

            status = res_json['status']

            return status=='OK'

        else:
            return False

    def send_text(self, text):

        param = {   'ID_DEST' : self.id_dest,
                    'ID_MITT' : self.user_id,
                    'text'    : text            }

        response = requests.get(url=self.api_url+self.api_method, params=param)

        res_json = response.json()

        status = res_json['status']

        return status=='OK'

    def run(self):

        while True:
            sent = False

            # Input message
            message_text = input('>>> ')

            command =  message_text.split(' ')[0]

            if command == '/file':
                if len( message_text.split(' ') ) >= 2:
                    path = message_text.split(' ')[1]

                    sent = self.send_file(path)

                    if sent:
                        print(f'\nFile {path} inviato correttamente.\n')
                    else:
                        print(f'\nErrore invio file. Controlla che {path} esista.\n')
                else:
                    print('\nErrore: formato del messaggio incorretto.\n')

            elif command == '/exit':
                break
            else:
                sent = self.send_text(message_text)

                if sent:
                    print(f'\nMessaggio inviato correttamente.\n')
                else:
                    print(f'\nErrore invio messaggio.\n')
