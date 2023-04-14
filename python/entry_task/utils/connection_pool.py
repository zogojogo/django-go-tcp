import gevent
from gevent.queue import Queue
import socket

class ConnectionPool:
    def __init__(self, host, port, size=None):
        self.host = host
        self.port = port
        self.size = size
        self.connections = Queue(maxsize=size) if size else None

    def get_connection(self):
        try:
            # connection pool
            conn = self.connections.get_nowait()
            print("get")
            print("queue lenght: {}".format(self.connections.qsize()))
        except gevent.queue.Empty:
            conn = socket.create_connection((self.host, self.port))
        return conn

    def release_connection(self, conn):
        try:
            self.connections.put_nowait(conn)
            print("release")
            print("queue lenght: {}".format(self.connections.qsize()))
        except gevent.queue.Full:
            conn.close()

    def close_all_connections(self):
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()