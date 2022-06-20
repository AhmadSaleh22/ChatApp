from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

from person import Person

# global CONSTANTS

HOST = ""
PORT = 5500
BUFSIZ = 512
MAX_CONNECTIONS = 10
ADDR = (HOST, PORT)

# GLOBAL VARS

persons = []

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # setup the server


def broadcast_message(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """

    for person in persons:
        client = person.client
        client.send(bytes(name, "utf8") + msg)


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
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat at {time.time()}", "utf8")
    broadcast_message(msg, "")

    while True:
        try:
            msg = client.recv(BUFSIZ)
            print(f"{name}: ", msg.decode("utf8"))
            if msg != bytes("{quit}", "utf8"):
                broadcast_message(f"{name} has left the chat ..", "")
                client.send(bytes("{quit}", "utf8"))
                client.close()
                persons.remove(person)
            else:
                broadcast_message(msg, name + ": ")
        except Exception as e:
            print("Exception", e)


def accept_incoming_connections():
    """
    Wait for connection from new clients, start new thread once connected
    :return: None
    """

    while True:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server {HOST} at time {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[SERVER ERR]", e)
            break

    print("Server Down Crashed ..")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # Listens for 5 connections at max.
    print("[STARTED]: Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
