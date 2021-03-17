import base64

from Crypto.Cipher import AES

from binascii import b2a_hex, a2b_hex





unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AES3:
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.iv = self.key

    def _pad(self, text):
        key_len = len(self.key)
        pad = text + (key_len - len(text) % key_len) * chr(key_len - len(text) % key_len)
        return pad

    def _unpad(self, text):
        pad = ord(text[-1:])
        return text[0:-pad]

    # 加密函数
    def encrypt(self, text):
        length = 16
        count = len(text)
        if count % length != 0:
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.iv.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(text, encoding="utf8"))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(b2a_hex(self.ciphertext)).decode('utf-8')

    # 解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.iv.encode("utf8"))
        plain_text = unpad(cryptor.decrypt(decode))
        return a2b_hex(plain_text) .decode('utf8')