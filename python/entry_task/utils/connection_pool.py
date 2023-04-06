import socket
from Queue import Queue

class ConnectionPool(object):
    def __init__(self, host, port, size):
        self.host = host
        self.port = port
        self.size = size
        self.connections = Queue(maxsize=size)

    def get_connection(self):
        try:
            conn = self.connections.get_nowait()
        except:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.host, self.port))
        return conn

    def release_connection(self, conn):
        try:
            self.connections.put_nowait(conn)
        except Queue.Full:
            conn.close()

    def close_all_connections(self):
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()