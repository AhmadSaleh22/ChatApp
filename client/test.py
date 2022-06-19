from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# global constants
HOST = 'localhost'
PORT = 5500
BUFSIZ = 512
# global vars

ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
messages = []


def recieve(messages):
    while True:
        client_socket.recv(BUFSIZ)

receive_thread = Thread(target=recieve)
receive_thread.start()