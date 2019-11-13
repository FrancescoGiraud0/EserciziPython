"""
Giraudo Francesco 
Github: @FrancescoGiraud0
Multithread server of the chat service.
"""

import serverSettings
import socket
import sqlite3
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP IPv4 socket creation

clients_online = {}  # Dictionary of IncomingMessageManager objects to manage incoming clients messages
connections_online = {}  # Dictionary of connections to send outgoing messages

class IncomingMessageManager(Thread):
    """
    Class having the task to receive message from a client, read the receiver nickname
    and send him that message.
    The incoming messages have the following format:
    RECEIVER_NICKNAME§MESSAGE§SENDER_NICKNAME
    """
    def __init__(self, conn, ip_address, port):
        Thread.__init__(self)
        self.conn = conn
        self.ip_address = ip_address
        self.port = port

    def run(self):
        msg = self.conn.recv(serverSettings.BUFFSIZE).decode() # Wait for new incoming messages
        print(f'Message: {msg}')
        
        try:
            # Split the message to get the nickaname of the receiver
            receiver_nickname, _, _ = msg.split('§', maxsplit=2)
            # Get the connection with {receiver_nickname}, if it is not online get the string "AAA not online"
            conn_to_receiver = connections_online.get(receiver_nickname, f"{receiver_nickname} not online")

            if not isinstance(conn_to_receiver, str):
                conn_to_receiver.send(msg.encode()) # Send the message
            else:
                print(conn_to_receiver)
        except ValueError:
            print(f'#ERROR# {self.ip_address}:{self.port} -> Incoming message format error!')


class NewConnectionsManager(Thread):
    """
    Class having the task to manage new client connections and checking if
    the client connected is in the database.
    """
    def __init__(self, server_ip, server_port, max_clients):
        Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = server_port
        self.max_clients = max_clients

    def run(self):
        sock.bind((self.server_ip, self.server_port))

        try:
            while True:
                sock.listen(self.max_clients)

                db = sqlite3.connect(serverSettings.DB_NAME) # Creations of new instance of database object
                cursor = db.cursor()

                try:
                    conn, (address, port) = sock.accept()
                    print(f'{address}:{port} connected.')
                except InterruptedError:
                    print('#ERROR# InterruptedError during accept!')

                newClientThread = IncomingMessageManager(conn, address, port)
                
                # Get all elements with ip_address = address
                cursor_iterator = cursor.execute(f"SELECT nick_name FROM CLIENT WHERE ip_address = '{address}'")
                # Get the first element of cursor_iterator (tuple) using fetchone()
                nickname = cursor_iterator.fetchone()[0]

                if not nickname == None:
                    # Start the thread
                    newClientThread.start()
                    # Save that thread in a dictionary where the key is a nickname
                    clients_online[nickname] = newClientThread
                    # Store the connection (object) between client and server in connections_online dictionary
                    connections_online[nickname] = conn
                    print(f"{nickname} is ONLINE.")
                else:
                    conn.close() # Close the connection if there is no users with that ip address in the database
                
                db.close() # Close the database

        except InterruptedError:
            db.close()
            map(lambda client: client.join(), clients_online)
            map(lambda connection: connection.close(), connections_online)
            sock.close()

if __name__ == '__main__':
    newConnectionsManager = NewConnectionsManager("0.0.0.0", serverSettings.PORT, serverSettings.MAX_CLIENTS)
    newConnectionsManager.start()
