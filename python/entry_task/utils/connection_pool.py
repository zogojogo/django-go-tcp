import socket

class ConnectionPool(object):
    def __init__(self, host, port, size):
        self.host = host
        self.port = port
        self.size = size
        self.connections = []

    def get_connection(self):
        if len(self.connections) < self.size:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.host, self.port))
            self.connections.append(conn)
        else:
            conn = self.connections.pop()
        return conn

    def release_connection(self, conn):
        self.connections.append(conn)

    def close_all_connections(self):
        for conn in self.connections:
            conn.close()