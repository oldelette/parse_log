import json
from output.type import OutputModule as OurModule

class OutputModule(OurModule):
    def __init__(self, args=None):
        """Initialize the single object JSON output module"""
        self.name = 'sojson'
        self.desc = 'output to a single JSON object'

        if args:
            args.add_argument('--sojson', action='store', dest='sojson',
                    help='set the output file for single object JSON output')
            args.add_argument('--pretty', action='store_true', dest='pretty',
                    help='use pretty formatting for sojson output')

    def write_output(self, data, args=None, filename=None, pretty=False):
        """Write log data to a single JSON object"""
        if args:
            if not args.sojson:
                return 0
            pretty = args.pretty
        if not filename: filename = args.sojson
        if pretty:
            logstring = json.dumps(
                    data['entries'], indent=2, sort_keys=True,
                    separators=(',', ': '))
        else:
            logstring = json.dumps(data['entries'], sort_keys=True)
        
        with open(str(filename), 'w') as output_file:
            output_file.write(logstring)
