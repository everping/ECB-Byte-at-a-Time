from Crypto.Cipher import DES, DES3, AES
from twisted.internet import protocol, reactor

SECRET = "everpingzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
# Now Support: "AES", "3DES", "DES"
ALGORITHM = "AES"
KEY = "17fb7b0b3069ddf79de9a21c"
PORT = 1234


class Oracle:
    """
    This is a encryption class using the Block Cipher with ECB mode and it is the weakness of this system
    """
    def __init__(self, algorithm, key):
        self.algorithm = algorithm
        self.key = key
        self.cryptor = self.get_cryptor()

    def get_block_size(self):
        if self.algorithm is "AES":
            return 16
        elif self.algorithm is "3DES":
            return 8
        if self.algorithm is "DES":
            return 8

    def get_cryptor(self):
        if self.algorithm is "AES":
            return AES.new(self.key, AES.MODE_ECB)
        elif self.algorithm is "3DES":
            return DES3.new(self.key, DES3.MODE_ECB)
        elif self.algorithm is "DES":
            return DES.new(self.key, DES.MODE_ECB)

    def pad(self, data):
        # PKCS#5 padding
        block_size = self.get_block_size()
        pad_len = block_size - len(data) % block_size
        pad_data = chr(pad_len) * pad_len
        return data + pad_data

    def unpad(self, data):
        pad_len = ord(data[-1])
        return data[:-pad_len]

    def encrypt(self, data):
        data = self.pad(data)
        return self.cryptor.encrypt(data).encode('hex')

    def decrypt(self, data):
        result = self.cryptor.decrypt(data.decode("hex"))
        return self.unpad(result)


class Server(protocol.Protocol):
    def __init__(self):
        self.secret = SECRET
        self.algorithm = ALGORITHM
        self.key = KEY
        self.oracle = Oracle(self.algorithm, self.key)

    def connectionMade(self):
        msg = '''
        Welcome to the Cryptography System
        To encrypt, enter "encrypt [plaintext]". Ex, encrypt 123
        To decrypt, enter "decrypt [ciphertext]". Ex, encrypt 97e0327bda9789cb74c9e6abe22237fa
        \r\n > '''
        self.transport.write(msg)

    def dataReceived(self, data):
        try:
            data = data.strip().split(" ")
            print (data)
            if data[0] == "encrypt":
                response = self.oracle.encrypt(data[1] + SECRET)
            elif data[0] == "decrypt":
                response = self.oracle.decrypt(data[1])
            else:
                raise
            self.transport.write(" > " + response + "\r\n > ")
        except:
            self.transport.write(" > Something is wrong here\r\n > ")


def main():
    factory = protocol.ServerFactory()
    factory.protocol = Server
    reactor.listenTCP(PORT, factory)
    reactor.run()


if __name__ == '__main__':
    main()
