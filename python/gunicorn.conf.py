import multiprocessing

bind = "0.0.0.0:8000"
workers = 10
worker_class = "gevent"
worker_connections = 1000
