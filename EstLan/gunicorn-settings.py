#bind = "0.0.0.0:8000"
bind = "unix:/tmp/gunicorn_EstLan.sock"

workers = 2
proc_name = "EstLan"
#loglevel = 'debug'
