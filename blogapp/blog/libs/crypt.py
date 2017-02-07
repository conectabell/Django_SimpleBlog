# -*- coding: utf-8 -*-
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
#import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')


class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        try:
            raw = self._pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))
        except Exception as e:
            print "Error-Encrypt: " + str(e)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return (s +
            (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
