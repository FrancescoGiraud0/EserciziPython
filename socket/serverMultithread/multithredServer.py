import socket
from threading import Thread 
from functools import reduce

class ServerThread(Thread):

    def __init__(self, connection, client_ip, client_port, close_msg):
        Thread.__init__(self)
        self.connection = connection    # istance of Connection object
        self.client_ip = client_ip      # ip address of the client
        self.client_port = client_port  # comunication port of the client process
        self.connection_closed = False  # True if connection is closed
        self.close_msg = close_msg      # The string to send to close connection
        print(f"*** Established connection with {client_ip}:{client_port} ***")

    def isConnectionClosed(self):
        return self.connection_closed

    def closeConnection(self):
        self.connection.close() # close the connection
        self.connection_closed = True # set the connection_closed to True
        print(f"*** Closed connection with {self.client_ip}:{self.client_port} ***")

    def run(self):
        while True:
            msg = self.connection.recv(4096).decode()       # receive the message and decode it

            if msg == self.close_msg:  # check if the client send the close connection message
                self.closeConnection()                      # if True close the connection and exit from the while loop
                break
            else:
                print(f"From {self.client_ip}:{self.client_port} > {msg}")
                self.connection.send(msg.encode())

class ServerThreadsManager(Thread):

    def __init__(self, server_ip, server_port, max_clients, close_msg):
        Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = server_port
        self.max_clients = max_clients
        self.close_msg = close_msg
        self.serverThreadsList = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # TCP IPv4 socket creation

    def checkConnectionsClosed(self):
        closed_connections = False
        if len(self.serverThreadsList) > 0:
            # check if there is almost one connection closed, it's an alternative to for loop
            conn_status_list = list(map(lambda x: x.isConnectionClosed(), self.serverThreadsList))
            print(f"conn_status: {conn_status_list}")
            closed_connections = reduce((lambda x,y: x or y), conn_status_list)
        print(f"cc: {closed_connections}")
        return closed_connections   # return True if there is almost one closed connection, False if not
    
    def closeAllConnections(self):
        map(lambda x: x.closeConnection(), self.serverThreadsList)  # apply the function close all connections to al threads
        map(lambda x: x.join(), self.serverThreadsList)             # stop all threads
        self.serverThreadsList.clear()
    
    def closeSocket(self):
        self.sock.close()
    
    def newConnections(self):
        while True:
            self.sock.listen(self.max_clients) # listen to new clients
            try:
                connection, (ip, port) = self.sock.accept()                  # new connection
            except:
                print("### NEW CONNECTIONS ERROR ###")
                break
            
            newThread = ServerThread(connection, ip, port, self.close_msg)    # creation instance of serverThread class
            newThread.start()                                                 # starting the server
            self.serverThreadsList.append(newThread)                          # append the serverThread in a list

    def run(self):
        self.sock.bind((self.server_ip, self.server_port))  # bind ip and port of server

        newConnectionsThread = Thread(target = self.newConnections)

        print(f"--- Listening new connections on port {self.server_port} ---")

        newConnectionsThread.start()    # from here server starts wait for new connections

        # loop to stop server when almost one client close the connection
        while True:
            if self.checkConnectionsClosed():
                newConnectionsThread.join()
                break

        self.closeAllConnections()
        self.sock.close()
