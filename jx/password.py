# coding=utf-8

import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AES3:
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.iv = self.key
        self.ciphertext = ''

    # 加密函数
    def encrypt(self, text):
        length = 16
        count = len(text)
        add = length - (count % length) if count % length != 0 else 0
        text = text + ('\0' * add)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.iv.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(text, encoding="utf8"))

        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(b2a_hex(self.ciphertext)).decode('utf-8')

    # 解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text.encode('utf-8'))
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.iv.encode("utf8"))
        plain_text = cryptor.decrypt(a2b_hex(decode))
        return plain_text.decode('utf8').rstrip('\0')


pc = AES3('boomboomboomboom')


if __name__ == "__main__":

    enc = pc.encrypt('111111')
    print(enc)

    dec = pc.decrypt(enc)
    print(dec)

    exit(0)
