from multiprocessing import shared_memory
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client:
    """
    for communication with the server:
    """

    # constants

    HOST = "localhost"
    PORT = 5500
    BUFSIZ = 512
    ADDR = (HOST, PORT)

    def __int__(self, name):
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

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()
                self.messages.append(msg)
                print(msg)
            except Exception as e:
                print("[Exception] ", e)
                break

    def send_message(self, msg):
        # encoding the data once it sent to one of stream member
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        """
        :return: listed of string messages
        :returns: list[str]
        """
        return self.messages
