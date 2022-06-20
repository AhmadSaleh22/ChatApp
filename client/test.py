import time

from client import Client
from threading import Thread

c1 = Client("AhmadSaleh")
c2 = Client("MoeSaleh")


def update_messages():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update every 1/10 of a second
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        for msg in new_messages:  # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break


c1.send_message("Hi Moe")
time.sleep(5)
c2.send_message("Hi Ahmad, How are you")
time.sleep(5)
c1.send_message("Fine thank you, hby ?")
time.sleep(5)
c2.send_message("all good")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()

