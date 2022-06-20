import threading
from multiprocessing import shared_memory
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock


class Client:
    """
    for communication with the server:
    """

    # constants

    HOST = "localhost"
    PORT = 5500
    BUFSIZ = 512
    ADDR = (HOST, PORT)

    def __init__(self, name):
        """
        Init object and send name to server
        :param name:
        :return:
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCPETION]", e)
                break

    def send_message(self, msg):
        # encoding the data once it sent to one of stream member
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        """
        :return: listed of string messages
        :returns: list[str]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy

    def disconnect(self):
        self.send_message(bytes("{quit}", "utf8"))
