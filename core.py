import os
import sys
import string
import parsers
import output
from parsers import syslog
from argparse import ArgumentParser

class LogDissectCore:

    def __init__(self):
        """Initialize logdissect job"""
        self.input_files = []
        self.parse_modules = {}
        self.filter_modules = {}
        self.output_modules = {}
        self.data_set = {}
        self.args = None
        self.arg_parser = ArgumentParser()
        self.output_args = self.arg_parser.add_argument_group('output options')

    def load_parsers(self):
        """Load parsing module(s)"""
        for parser in sorted(parsers.__all__):
            self.parse_modules[parser] = \
                __import__('parsers.' + parser, globals(), \
                locals(), ['parsers']).ParseModule()
                # __import__('parsers.' + parser, globals(),locals()).ParseModule()

    def load_outputs(self):
        """Load output module(s)"""
        for out in sorted(output.__formats__):
            self.output_modules[output] = \
                __import__('output.' + out, globals(), \
                locals(), ['output']).OutputModule(args=self.output_args)


    def config_args(self):
        """Set config options"""
        # Module list options:
        self.arg_parser.add_argument('files',
                metavar='file', nargs='*',
                help=('specify input files'))
        self.arg_parser.add_argument('-p',
                action='store', dest='parser', default='syslog',
                help=('select a parser (default: syslog)'))
        self.arg_parser.add_argument('-t',
                action='store', dest='tzone',
                help=('specify timezone offset to UTC (e.g. \'+0500\')'))
        self.args = self.arg_parser.parse_args()

    # run_job does the actual job using the other functions.
    def run_job(self):
        """Execute a logdissect job"""
        self.load_parsers()
        self.load_outputs()
        self.config_args()
        self.load_inputs()
        self.run_parse()
        self.run_output()

    # Load input files:
    def load_inputs(self):
        """Load the specified inputs"""
        for f in self.args.files:
            if os.path.isfile(f):
                fparts = str(f).split('.')
                if fparts[-1] == 'gz':
                    if self.args.unzip:
                        fullpath = os.path.abspath(str(f))
                        self.input_files.append(fullpath)
                    else:
                        return 0
                elif fparts[-1] == 'bz2' or fparts[-1] == 'zip':
                    return 0
                else:
                    fullpath = os.path.abspath(str(f))
                    self.input_files.append(fullpath)
            else:
                print('File '+ f + ' not found')
                return 1

    def run_parse(self):
        """Parse one or more log files"""
        # Data set already has source file names from load_inputs
        print("start parse: ", self.args.files)
        parsedset = {}
        parsedset['data_set'] = []
        print(self.args)
        for log in self.input_files:
            parsemodule = self.parse_modules[self.args.parser]
            try:
                if self.args.tzone:
                    parsemodule.tzone = self.args.tzone
            except NameError: pass
            parsedset['data_set'].append(parsemodule.parse_file(log))
        self.data_set = parsedset
        del(parsedset)

    def run_output(self):
        """Output finalized data"""
        for f in output.__formats__:
            ouroutput = self.output_modules[f]
            ouroutput.write_output(self.data_set['finalized_data'],
                    args=self.args)
            del(ouroutput)

        # Output to terminal if silent mode is not set:
        if not self.args.silentmode:
            if self.args.verbosemode:
                print('\n==== ++++ ==== Output: ==== ++++ ====\n')
            for line in self.data_set['finalized_data']['entries']:
                print(line['raw_text'])


def main():
    dissect = LogDissectCore()
    dissect.run_job()
                
if __name__ == "__main__":
    dissect = LogDissectCore()
    dissect.run_job()
