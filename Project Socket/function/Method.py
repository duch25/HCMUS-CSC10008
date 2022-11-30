import config
import os
from function.Response import *


class REQUEST:
    def __init__(self, request):
        request_lines = request.split("\r\n")
        # -> parsing Method (GET, POST...)
        self.method = request_lines[0].split(" ")[0]
        # -> parsing file name
        self.path = (request_lines[0].split(" ")[1])
        # -> parsing username, password.
        self.content = request_lines[-1]


def isCorrectLogin(loginMsg):
    msg = loginMsg.split("&")
    if ((msg[0] == f"uname={config.USERNAME}") and (msg[1] == f"psw={config.PASSWORD}")):
        return True
    return False


def POSTmethod(client, request, isPersistent, user):

    if isCorrectLogin(request.content):

        print("LOGIN SUCCESS.\n")

        try:
            client.sendall(
                RESPONSE(config.IMAGE_FILE).makeResponse(isPersistent))
        except:
            pass

        config.clientLogined.append(user)
    else:
        print("LOGIN FAIL.\n")
        try:
            client.sendall(
                RESPONSE(config.UNAUTHORIZED_FILE).makeResponse(isPersistent))
        except:
            pass


def GETmethod(client, request, isPersistent, user):

    # response index.html or images.html when logged in successfully.
    if (request.path in ["/", "/index.html", "/index.html?"]):
        if user in config.clientLogined:
            request.path = config.IMAGE_FILE
        else:
            request.path = config.INDEX_FILE
    # handle access not allowed.
    elif request.path == "/images.html":
        if user in config.clientLogined:
            request.path = config.IMAGE_FILE
        else:
            request.path = config.UNAUTHORIZED_FILE
    # response 404 Not Found when request page does not exist.
    elif not os.path.exists(request.path.strip('/')):
        request.path = config.NOT_FOUND_FILE

    client.sendall(RESPONSE(request.path).makeResponse(isPersistent))
