import os

class Test():
    offset = 0

    @classmethod
    def get_last_line(cls):
        #filepath = self.parsefile
        filepath = "/var/log/atftpd.log"
        #global already_print_num
        data_set = []
        if not os.path.exists(filepath):
            print(f"no such file {filepath}")
            sys.exit()
            return
        readfile = open(filepath, "r")
        lines = readfile.readlines()
        print("**"*20)
        print("file size: ",readfile.tell(),"offset: ",cls.offset)
        cls.offset = readfile.tell()
        print("**"*20)
        readfile.close()
        return data_set


#Test.get_last_line()
#Test.get_last_line()
