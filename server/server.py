from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

from server.Person import Person
# global CONSTANTS

HOST = 'localhost'
PORT = 5500
BUFSIZ = 512
MAX_CONNECTIONS = 5
ADDR = (HOST, PORT)

# GLOBAL VARS

persons = []


def broadcast_message(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """

    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", "utf8") + msg)


def client_communication(person):
    """
        Thread to handle all messages from client
        :param person: Person
        :return: None
    """

    run = True
    client = person.client
    # name = person.name
    addr = person.addr

    # get person's name
    name = client.recv(BUFSIZ).decode("utf8")
    person.__set_name__(name)

    msg = bytes(f"{name} has joined the chat at {time.time()}", "utf8")
    broadcast_message(msg)

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}","utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            persons.remove(person)
        else:
            client.send(msg, name)


def accept_incoming_connections():
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr,client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server {HOST} at time {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[SERVER ERR]", e)
            run = False
    print("Server Down Crashed ..")



SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # Listens for 5 connections at max.
    print("[STARTED]: Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
