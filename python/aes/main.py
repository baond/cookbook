import base64
from Crypto.Cipher import AES
from Crypto import Random
from sys import argv
import traceback

secret_key32 = "SDDHUI782KNJ2SDFJAF982WEFG982NIF"

class AESCipher:
    def __init__( self, key ):
        self.key = key
        self.BS = 16
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * '\0'
        self.unpad = lambda s: s.rstrip('\0')

    def encrypt( self, raw ):
        raw = self.pad(raw)
        iv = Random.new().read( self.BS )    # AES.block_size is 16
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        enc = cipher.encrypt(raw)
        return base64.b64encode( iv + enc )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:self.BS]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return self.unpad(cipher.decrypt( enc[self.BS:] ))

if __name__ == "__main__":
    if len(argv) > 3:
        secret_key32 = argv[3]
    cipher = AESCipher(secret_key32)
    try:
        if argv[1] == "-e":
            print(cipher.encrypt(argv[2]))
        elif argv[1] == "-d":
            print(cipher.decrypt(argv[2]))
    except Exception as e:
        traceback.print_exc()
