from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# global constants
HOST = "localhost"
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)

# global vars

messages = []
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def receive_messages():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[Exception] ", e)
            break


def send_message(msg):
    # encoding the data once it sent to one of stream member
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()


receive_thread = Thread(target=receive_messages)
receive_thread.start()


send_message("Ahmad Saleh")
send_message("Hi Saleh")
send_message("Hi Saleh")
