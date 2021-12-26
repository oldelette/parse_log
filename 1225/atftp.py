import os
import sys
import json
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
from dataclasses import dataclass


@dataclass
class ParseModule:
    timestamp: str
    hostname: str
    appname: str
    pidnum: str
    message: str

@dataclass
class ServiceModule:
    filename: str
    ip: str
    #start: str
    #end: str
    success: bool


@dataclass
class Parser(object):
    parsefile: str
    already_print_num: int = 0   
 # run_job does the actual job using the other functions.
    def run_job(self):
        """Execute a parser job"""
        try:
            # self.load_rule()
            # self.load_parse()
            self.parse_file()
        except KeyboardInterrupt:
            sys.exit(1)


    def atftp_rule(self):
        ints = Word(nums)
        month = Word(string.ascii_uppercase, string.ascii_lowercase, exact=3)
        day = ints
        hour = Combine(ints + ":" + ints + ":" + ints)
        rule1 = month + day + hour  # timestamp
        rule2 = Word(alphas + nums + "_" + "-" + ".")  # hostname
        rule3 = Word(alphas + "/" + "-" + "_" + ".")  # appname
        rule4 = Combine("[" + ints + "." + ints + "]:")  # pidnum
        rule5 = Regex(".*")  # message

        return rule1 + rule2 + rule3 + rule4 + rule5

    def service_rule(self):
        msg1 = Word(alphas)
        fname = Word(alphas + nums + "_" + "-" + ".")
        msg2 = Word(alphas, exact=2)
        ip_field = Word(nums, max=3)
        ip_addr = Combine( ip_field + "." + ip_field + "." + ip_field + "." + ip_field )
        return msg1 + fname + msg2 + ip_addr

    def load_parse(self, line:str) -> dict:
        rule = self.atftp_rule()
        parsed = rule.parseString(line)

        return vars(
            ParseModule(
                timestamp=strftime("%Y-%m-%d %H:%M:%S"),
                hostname=parsed[3],
                appname=parsed[4],
                pidnum=parsed[5],
                message=parsed[6],
            )
        )

    def get_last_line(self):
        filepath = self.parsefile
        #global already_print_num
        data_set = []
        if not os.path.exists(filepath):
            print(f"no such file {filepath}")
            sys.exit()
            return
        readfile = open(filepath, "r")
        lines = readfile.readlines()
        if len(lines) > 6 and self.already_print_num == 0:
            self.already_print_num = len(lines) - 6
    
        if self.already_print_num < len(lines):
            print_lines = lines[self.already_print_num - len(lines) :]
            for line in print_lines:
                data_set.append(self.load_parse(line))
                #print(line.replace("\n", ""))
            self.already_print_num = len(lines)
        readfile.close()
        return data_set

    def parse_file(self):
        """Parse single JSON object into a LogData object"""
        data_set = []
        sourcepath = self.parsefile
        with open(sourcepath, 'r') as logfile:
            for line in logfile:
                data_set.append(self.load_parse(line))

        #print(data_set)
        #logstring = json.dumps(data_set, indent=2, sort_keys=True,separators=(',', ': '))
        #print(logstring)
        
        return data_set

    def fliter_service(self):
        service_set = []
        error_list = ["not responding","not found"]
        #data_set = self.parse_file()
        data_set = self.get_last_line()
        start,end = 0,0
        state,flag = True,True
        for data in data_set:
            if any([True for error in error_list if error in data["message"]]):
                state = False
            
            if data["message"] == "socket may listen on any address, including broadcast":
                start = data["timestamp"]
                #print(data["message"])
            elif "Serving" in data["message"] and flag:
                #print(data["message"])
                rule = self.service_rule()
                parsed = rule.parseString(data["message"])
                flag = False
                #print(parsed)
            elif data["message"] == "Server thread exiting" and not flag:
                end = data["timestamp"]
                #service_set.append(vars(ServiceModule(parsed[1],parsed[3],start,end,state)))
                print("**"*20)
                service_set.append(vars(ServiceModule(parsed[1],parsed[3],state)))
                state = True
                flag = True
        #return service_set
        return [dict(s) for s in set(frozenset(d.items()) for d in service_set)]

#def main():
#    #parser = Parser("/var/log/atftpd.log")
#    parser = Parser("/tmp/atftpd.log")
#    #parser.parse_file()
#    res = parser.fliter_service()
#    print(res)
#    #parser.run_job()
#    # syslogPath = sys.argv[1]
#
#if __name__ == "__main__":
#    main()