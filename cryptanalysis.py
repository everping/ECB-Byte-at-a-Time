import socket
import string

ALGORITHM = "AES"
HOST = "127.0.0.1"
PORT = 1234


class Cryptanalysis:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.charset = string.ascii_letters
        self.guess_multiples = 1
        self.client = Client()

    def get_block_size(self):
        if self.algorithm is "AES":
            return 16
        elif self.algorithm is "3DES":
            return 8
        if self.algorithm is "DES":
            return 8

    def guess_max_size_secret(self):
        block_size = self.get_block_size()
        return block_size * self.guess_multiples

    def break_it(self):
        while True:
            max_size_secret = self.guess_max_size_secret()
            try:
                secret = ""
                for size in range((max_size_secret - 1), -1, -1):
                    origin = "A" * size
                    self.client.send(origin)
                    origin_response = self.client.receive()

                    tmp = "A" * size + secret
                    for character in self.charset:
                        self.client.send(tmp + character)
                        tmp_response = self.client.receive()

                        if origin_response.decode("hex")[:max_size_secret] == tmp_response.decode("hex")[
                                                                              :max_size_secret]:
                            secret += character
                            break
                    if len(secret) + size <= max_size_secret - 1:
                        return secret
            except:
                self.guess_multiples += 1


class Client:
    def __init__(self):
        self.socket = self.init_socket()
        self.receive()

    @staticmethod
    def init_socket():
        client = socket.socket()
        client.connect((HOST, PORT))
        return client

    @staticmethod
    def normalize(data):
        return data.strip(" > ").strip()

    def receive(self):
        return self.normalize(self.socket.recv(1024))

    def send(self, data):
        self.socket.send(self.rebuild(data))

    @staticmethod
    def rebuild(data):
        return "encrypt %s \n" % data


cryptanalysis = Cryptanalysis(ALGORITHM)
print (cryptanalysis.break_it())
