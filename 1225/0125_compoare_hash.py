from __future__ import annotations
import os
import hashlib
from dataclasses import dataclass, field

@dataclass
class History:
    ack_offset:int = 0
    # size: int = 0
    hash_val:str = ""


@dataclass
class Tail:
    _offset:int = 0
    _ack_offset:int = 0
    last_size: int = 0
    parsefile:str = ""
    # tmp_history:History = field(default_factory=dict)
    tmp_history:History = field(default_factory=History)

    @classmethod
    def md5(cls, offset: int):
        if offset < 500:
            cls._ack_offset = offset
        else:
            offset = 500
            cls._ack_offset = offset
        hash_md5 = hashlib.md5()
        with open(cls.parsefile, "rb") as f:
            chunk = f.read(offset)
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @classmethod
    def set_history(cls, parse):
        cls.parsefile = parse
        if not cls.last_size:
            tmp_history = History(cls.last_size, )
            print(f"tmp hist: {tmp_history}")

        # tmp_history = History(cls.last_size, cls.md5(cls.last_size))
    # same file or not
    # def judge():

    @classmethod
    def get_last_line(cls):
        filepath = cls.parsefile
        data_set = []
        if not os.path.exists(filepath):
            print(f"no such file {filepath}")
        #readfile = open(filepath, "r")
        with open(filepath, 'r', encoding="utf-8") as readfile:
            readfile.seek(cls._offset,0)
            data_set = readfile.readlines()
            print("**"*20)
            print("file size: ",readfile.tell(),"ack_offset: ",cls._offset)
            cls.last_size = cls._offset
            cls._offset = readfile.tell()
        return data_set

file = '/home/gavin/gavin/parselog/atftpd.log'

while(1):
    a = int(input("input:"))
    if a == 1:
        Tail.set_history(file)
        test = Tail.get_last_line()
        print(test)

# a = md5(file)
print(f"size {os.path.getsize(file)}")
