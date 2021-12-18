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
class Parser(object):
    
 # run_job does the actual job using the other functions.
    def run_job(self):
        """Execute a parser job"""
        try:
            # self.load_rule()
            # self.load_parse()
            self.parse_file()
        except KeyboardInterrupt:
            sys.exit(1)


    def load_rule(self):
        ints = Word(nums)
        month = Word(string.ascii_uppercase, string.ascii_lowercase, exact=3)
        day = ints
        hour = Combine(ints + ":" + ints + ":" + ints)
        rule1 = month + day + hour  # timestamp
        rule2 = Word(alphas + nums + "_" + "-" + ".")  # hostname
        rule3 = Word(alphas + "/" + "-" + "_" + ".")  # appname
        rule4 = Combine("[" + ints + "." + ints + "]")  # pidnum
        rule5 = Regex(".*")  # message

        return rule1 + rule2 + rule3 + rule4 + rule5

    def load_parse(self, line):
        rule = self.load_rule()
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

    def parse_file(self):
        """Parse single JSON object into a LogData object"""
        data_set = []
        sourcepath = sys.argv[1]
        with open(sourcepath, 'r') as logfile:
            for line in logfile:
                data_set.append(self.load_parse(line))

        #print(data_set)
        #logstring = json.dumps(data_set, indent=2, sort_keys=True,separators=(',', ': '))
        #print(logstring)
        

def main():
    parser = Parser()
    parser.run_job()
    # syslogPath = sys.argv[1]

if __name__ == "__main__":
    main()
