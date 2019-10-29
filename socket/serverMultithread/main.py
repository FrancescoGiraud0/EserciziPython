import serverSettings
import multithredServer as mts

server = mts.ServerThreadsManager(serverSettings.IP_ADDRESS, serverSettings.PORT,
                                  serverSettings.MAX_CLIENTS, serverSettings.CLOSE_CONNECTION_MSG)

print("Starting server...")
server.start()

server.join()
