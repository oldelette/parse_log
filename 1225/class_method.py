import os
import hashlib

class Tail():
    _offset = 0
    _last_hast = ""

    def __init__(self,parse):
        Tail.parsefile = parse

    @classmethod
    def get_last_line(cls):
        cls.check_md()
        filepath = cls.parsefile
        #filepath = "/var/log/atftpd.log"
        #global already_print_num
        data_set = []
        if not os.path.exists(filepath):
            print(f"no such file {filepath}")
            sys.exit()
            return
        #readfile = open(filepath, "r")
        with open(filepath, 'r', encoding="utf-8") as readfile:
            readfile.seek(cls._offset,0)
            data_set = readfile.readlines()
            print("**"*20)
            print("file size: ",readfile.tell(),"offset: ",cls._offset, "data: ",data_set)
            cls._offset = readfile.tell()
        #readfile.close()
        return data_set
    
    @classmethod
    def check_md(cls):
        hash1 = hashlib.md5()
        with open(cls.parsefile, 'r', encoding="utf-8") as readfile:
            readfile.seek(500,0)
            chk = readfile.read()
            hash1.update(chk.encode('UTF-8'))
            hash1 = hash1.hexdigest()
            print("md5: ", hash1, chk)
        return hash1

#Test.get_last_line()
#Test.get_last_line()
