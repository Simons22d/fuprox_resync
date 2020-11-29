import socketio
from datetime import datetime
import time

from fuprox.models.models import (Branch, BranchSchema)

link = "http://localhost:4000"

# online socket link
# socket_link = "http://159.65.144.235:5000/"

#  offline socket link
socket_link = "http://localhost:5000/"

# standard Python
sio = socketio.Client()

# branch schema
branch_schema = BranchSchema()
branches_schema = BranchSchema(many=True)


def log(msg):
    print(f"{datetime.now().strftime('%d:%m:%Y %H:%M:%S')} — {msg}")
    return True


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


try:
    sio.connect(socket_link)
except socketio.exceptions.ConnectionError:
    print("Error! Could not connect to the socket server.")



while True:
    branches = Branch.query.all()
    for branch in branches:
        sio.emit("init_sync", {"key": branch.key_})
        log("init offline synce √")
    time.sleep(10)
