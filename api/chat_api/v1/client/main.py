import config
import requests
import sqlite3 as sqlite
from MessageReceiver import MessageReceiver
from MessageSender import MessageSender

REQ_MESSAGES_QUERY = '''SELECT m.msg_timestamp, c.nome, c.cognome, m.message 
FROM messages AS m INNER JOIN contacts as c ON m.id_mitt=c.id
WHERE c.blocked=0
ORDER BY m.msg_timestamp
'''
INSERT_CONTACTS_QUERY = 'INSERT OR IGNORE INTO contacts(id, nome, cognome) VALUES (?,?,?) ;'
REQ_CONTACTS_QUERY = 'SELECT id, nome, cognome FROM contacts'
BLOCK_UNBLOCK_USER = 'UPDATE contacts SET blocked=*b* WHERE id=*i* ;'

def print_messages():

    print('\nMessaggi in arrivo')

    conn = sqlite.connect(config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute(REQ_MESSAGES_QUERY)

    for c in cursor.fetchall():
        print(f'{c[0]} {c[1]} {c[2]} : {c[3]}')

    cursor.close()
    conn.close()

def update_users():
    response = requests.get(config.SERVER_URL+'/user_list')

    res_json = response.json()

    contacts = []

    if res_json['status']=='OK' and res_json['count']>=0:
        contacts = res_json['results']
        contacts_list = [(c['id'], c['name'], c['surname']) for c in contacts]

        conn = sqlite.connect(config.DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.executemany(INSERT_CONTACTS_QUERY, contacts_list)

            conn.commit()
        except:
            print('Errore DB.')
        finally:
            cursor.close()
            conn.close()
    else:
        print('Errore query.')

def print_contacts(blocked=False):
    conn = sqlite.connect(config.DB_PATH)
    cursor = conn.cursor()

    if blocked:
        query = REQ_CONTACTS_QUERY+' WHERE blocked=1;'
    else:
        query = REQ_CONTACTS_QUERY+' WHERE blocked=0'
    
    cursor.execute(query)

    contacts_list = []

    for c in cursor.fetchall():
        print(f'{c[0]}. {c[1]} {c[2]}')
        contacts_list.append(c[0])

    cursor.close()
    conn.close()

    return contacts_list

def blocca_utente():
    selection = ''
    while not selection=='0':
        print(f"\nSeleziona contatto da BLOCCARE")
        print('0. Esci')
        contacts = print_contacts(blocked=False)

        selection = input('>>> ')

        if int(selection) in contacts:
            conn = sqlite.connect(config.DB_PATH)
            cursor = conn.cursor()

            query = BLOCK_UNBLOCK_USER.replace('*b*', '1')
            query = query.replace('*i*', selection)

            cursor.execute(query)

            conn.commit()

            cursor.close()
            conn.close()
        elif selection == '0':
            pass
        else:
            print('\nUTENTE NON DISPONIBILE')

def sblocca_utente():
    selection = ''
    while not selection=='0':
        print(f"\nSeleziona contatto da SBLOCCARE")
        print('0. Esci')
        contacts = print_contacts(blocked=True)

        selection = input('>>> ')

        if int(selection) in contacts:
            conn = sqlite.connect(config.DB_PATH)
            cursor = conn.cursor()

            query = BLOCK_UNBLOCK_USER.replace('*b*', '0')
            query = query.replace('*i*', selection)

            cursor.execute(query)

            conn.commit()
            cursor.close()
            conn.close()
        elif selection == '0':
            pass
        else:
            print('\nUTENTE NON DISPONIBILE\n')

def invio_messaggio():
    selection = ''
    while not selection=='0':
        print(f"\nSeleziona destinatario")
        print('0. Esci')
        contacts = print_contacts(blocked=False)

        selection = input('>>> ')

        if int(selection) in contacts:
            ms = MessageSender( config.SERVER_URL, config.USER_ID, selection)
            ms.run()
            selection='0'
        elif selection=='0':
            pass
        else:
            print('\nCONTATTO NON DISPONIBILE')

def print_menu():
    print('\n0. Esci')
    print('1. Messaggi in arrivo')
    print('2. Invia messaggio')
    print('3. Blocca utente')
    print('4. Sblocca Utente')

def main_menu():
    selection = ''
    while not selection=='0':
        print_menu()
        selection = input('>>> ')

        if selection=='0':
            pass
        elif selection=='1':
            print_messages()
        elif selection=='2':
            invio_messaggio()
        elif selection=='3':
            blocca_utente()
        elif selection=='4':
            sblocca_utente()
        else:
            print('\nOPZIONE NON DISPONIBILE')

if __name__ == "__main__":
    mr = MessageReceiver( config.SERVER_URL, config.USER_ID, config.DB_PATH, config.MEDIA_FOLDER )
    
    print('Aggiornamento contatti...')
    update_users()
    
    mr.start()
    
    main_menu()

    mr.stop()
    mr.join()