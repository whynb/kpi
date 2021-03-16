# coding=utf-8

class FileSaveException(Exception):
    def __init__(self, _str):
        self._str = _str
        
    def __str__(self):
        return self._str


class UserAuthException(Exception):
    def __init__(self, _str):
        self._str = _str

    def __str__(self):
        return self._str
