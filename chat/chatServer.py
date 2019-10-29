"""
Giraudo Francesco 
Github @FrancescoGiraud0
Multithread server with the main
"""

import settings
import socket
import sqlite3
from threading import Thread

clients_online = {}
connection_online = {}

class ServerChatThread(Thread):
    
    def __init__(self, conn, ip_address, port):
        Thread.__init__(self)
        self.conn = conn
        self.ip_address = ip_address
        self.port = port

    def run(self):
        msg = self.conn.recv(settings.BUFFSIZE).decode()
        receiver_nickname, _, _ = msg.split('§') # Gestire eventuale eccezione

        conn_to_receiver = connection_online.get(receiver_nickname, "not_online")

        if not isinstance(conn_to_receiver, str):
            conn_to_receiver.send(msg.encode())
        

class NewConnectionsManager(Thread):

    def __init__(self, server_ip, server_port, max_clients, db_name):
        Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = server_port
        self.max_clients = max_clients
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # TCP IPv4 socket creation

        db = sqlite3.connect(db_name)
        self.db = db
        self.cursor = db.cursor()
    
    def run(self):
        self.sock.bind((self.server_ip, self.server_port))

        while True:
            self.sock.listen(self.max_clients)

            try:
                conn, (address, port) = self.sock.accept()
            except InterruptedError:
                print("#INTERRUPTED ERROR DURING ACCEPT#")

            newConnectionThread = ServerChatThread(conn, address, port)

            nickname_list = self.cursor.execute(f"SELECT nick_name FROM CLIENT WHERE ip_address = {address}")
            
            if len(nickname_list) == 1:
                clients_online[nickname_list[0]] = newConnectionThread
                connection_online[nickname_list[0]] = conn

if __name__ == '__main__':
    newConnectionsManager = NewConnectionsManager(settings.IP_ADDRESS, settings.PORT, settings.MAX_CLIENTS, settings.DB_NAME)
    newConnectionsManager.start()
