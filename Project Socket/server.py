import socket
import threading
import sys
import os
import config
from function.Method import *

global isPersitent
global isConcurrency

# create socket server.
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Error creating server socket: ", err)
    sys.exit(1)

# This setup to reuse socket.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# handle request from client.
def handle(client, address):
    try:
        while True:

            # connection manager.
            client.settimeout(10)
            try:
                data = client.recv(config.BUFFER).decode(config.FORMAT)
            except socket.timeout:
                print("Request Timed-Out!\n")
                client.close()
                break

            # client closed.
            if not data:
                print("No Request From Client!\n")
                client.close()
                break

            # distinguish clients via web browser and IP address.
            user = ""
            for item in data.split('\r\n', 10):
                if item.split(':')[0] == "User-Agent":
                    user = item
                    break
            user = user + str(address).split(',')[0]

            # parsing request from client.
            request = REQUEST(data)

            print(f"[CLIENT {address}] {request.method} {request.path}\n")

            # handle method request.
            if (request.method == "POST"):
                POSTmethod(client, request, isPersistent, user)
            elif (request.method == "GET"):
                GETmethod(client, request, isPersistent, user)
            else:
                print("HTTP Method Not Allowed!\n")
                break

            # base on http persistent or non-persistent.
            if not (isPersistent):
                client.close()
                break
    except OSError as e:
        print(str(e))
    finally:
        client.close()


def start():
    server.listen(5)
    while True:
        client, address = server.accept()
        print(f"[CLIENT {address}] CONNECTED.\n")

        try:
            if (isConcurrency):
                # start new thread to handle concurrency.
                thread = threading.Thread(
                    target=handle, args=(client, address))
                thread.start()
                # thread.join(10)
            else:
                handle(client, address)

        # stop server by keyboard.
        except KeyboardInterrupt:
            print("Shutting down...")
            client.close()
            server.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

# start server by argument command line.
# python server.py <x> <y>
# x = 1 if use http persistent, x = 0 if use http non-persistent
# y = 1 if handle multiple clients at a time, x = 0 if hanlde one client at a time


# example: python server.py 1 1.
if __name__ == '__main__':

    isPersistent = int(sys.argv[1])
    isConcurrency = int(sys.argv[2])

    addr = ""
    if (isConcurrency):
        addr = socket.gethostbyname(socket.gethostname())
    else:
        addr = config.HOST

    try:
        server.bind((addr, config.PORT))
        print(f"[SERVER] Listening on: http://{addr}:{config.PORT}\n")
    except socket.gaierror as err:
        print("Error in binding host and port: ", err)
        sys.exit(1)
    except socket.error as err:
        print("Error in connection!\n")
        sys.exit(1)

    start()
