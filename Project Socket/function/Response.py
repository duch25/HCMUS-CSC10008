import config


class RESPONSE:
    def __init__(self, path):
        self.file_buff = ''
        self.status = 200

        if path == config.NOT_FOUND_FILE:
            self.status = 404
        elif path == config.UNAUTHORIZED_FILE:
            self.status = 401

        # handle access page does not exist.
        try:
            if (self.file_buff == ''):
                self.buffer = open(path[1:], "rb")
        except:
            self.status = 404
            self.buffer = open(config.NOT_FOUND_FILE[1:], "rb")

        # create response header
        header = ""

        if self.status == 404:
            header += "HTTP/1.1 404 Not Found\r\n"
        elif self.status == 401:
            header += "HTTP/1.1 401 Unauthorized\r\n"
        else:
            header += "HTTP/1.1 200 OK\r\n"

        # parsing Content-Type
        self.file_type = path.split('/')[-1].split('.')[-1]

        if self.file_type in ["html", "css"]:
            header += f"Content-Type: text/{self.file_type}\r\n"
        elif self.file_type in ["png", "ico", "jpg"]:
            extension = ""
            if self.file_type == "jpg":
                extension = "jpeg"
            else:
                extension = self.file_type
            header += f"Content-Type: image/{extension}\r\n"
        else:
            header += "Content-Type: application/octet-stream\r\n"

        self.header = header

    def makeResponse(self, isPersistent):
        if self.file_buff != '':
            content = self.file_buff.encode()
        else:
            content = self.buffer.read()

        if (isPersistent):
            # http persistent.
            self.header += f"Content-Length: {len(content)}\r\n\r\n"
        else:
            # http non-persistent.
            self.header += "Connection: close\r\n\r\n"

        responseMsg = self.header.encode() + content

        return responseMsg
