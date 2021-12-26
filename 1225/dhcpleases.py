import re
import datetime

try:
    utc = datetime.timezone.utc
except AttributeError:
    class UTC(datetime.tzinfo):
        def fromutc(self, dt):
            return dt

        def utcffset(self, dt):
            return datetime.timedelta(0)

        def dst(self, dt):
            return None

        def tzname(self, dt):
            return 'UTC'


    utc = UTC()

def check_datetime(dt):
    if not (dt is None or (isinstance(dt, datetime.datetime) and dt.tzinfo)):
        raise ValueError('None or offset-aware datetime required')

def parse_time(s):
    """
    Like datetime.datetime.strptime(s, "%w %Y/%m/%d %H:%M:%S") but 5x faster.
    """
    result = None

    if "epoch" in s:
        epoch_time = float(s.rstrip().split(' ')[1][:-1])
        result = datetime.datetime.utcfromtimestamp(epoch_time)
    else:
        _, date_part, time_part = s.split(' ')
        year, mon, day = date_part.split('/')
        hour, minute, sec = time_part.split(':')
        result = datetime.datetime(*map(int, (year, mon, day, hour, minute, sec)))

    return result.replace(tzinfo=utc)

def _extract_prop_option(line):
    """
    Extract the (key,value)-tuple from a string like:
    >>> "option foobar 123"
    :param line:
    :return: tuple (key, value)
    """
    line = line[7:]
    pos = line.find(' ')
    return line[:pos], line[pos + 1:]


def _extract_prop_set(line):
    """
    Extract the (key, value)-tuple from a string like:
    >>> 'set foo = "bar"'
    :param line:
    :return: tuple (key, value)
    """
    token = ' = "'
    line = line[4:]
    pos = line.find(token)
    return line[:pos], line[pos + 4:-1]

def _extract_prop_general(line):
    """
    Extract the (key, value)-tuple from a "standard" property line like:
    >>> 'hardware ethernet 12:34:56:78:90:AB'
    :param line:
    :return: tuple (key, value)
    """
    pos = line.find(' ')
    return line[:pos], line[pos + 1:]

def _extract_properties(config):
    """
    Parse a line within a lease block
    The line should basically match the expression:
    >>> r"\s+(?P<key>(?:option|set)\s+\S+|\S+) (?P<value>[\s\S]+?);"
    For easier seperation of the cases and faster parsing this is done using substrings etc..
    :param config:
    :return: tuple of properties dict, options dict and sets dict
    """
    general, options, sets = {}, {}, {}
    for line in config.splitlines():

        # skip empty & malformed lines
        if not line or not line[-1:] == ';' and '; #' not in line:
            continue

        # strip the trailing ';' and remove any whitespaces on the left side
        line = line[:-1].lstrip()

        # seperate the three cases
        if line[:6] == 'option':
            key, value = _extract_prop_option(line)
            options[key] = value

        elif line[:3] == 'set':
            key, value = _extract_prop_set(line)
            sets[key] = value

        else:
            # fall through to generic case
            key, value = _extract_prop_general(line)
            general[key] = value

    return general, options, sets

class BaseLease(object):
    """
    Base Implementation for all leases. This does most of the common work that is shared among v4 and v6 leases.
    Attributes:
        ip          The IP address assigned by this lease as string
        data        Dict of all the info in the dhcpd.leases file for this lease
        options     Options on this lease
        sets        Dict of key-value set statement values from this lease
    """

    def __init__(self, ip, properties, options=None, sets=None, now=None):
        check_datetime(now)

        if options is None:
            options = {}

        if sets is None:
            sets = {}

        self.ip = ip
        self.data = properties
        self.options = options
        self.sets = sets
        _, self.binding_state = properties['binding'].split(' ', 1)
        self._now = now

    @property
    def active(self):
        """
        Shorthand to check if the binding_state is active
        :return: bool: True if lease is active
        """
        return self.binding_state == 'active'

    @property
    def now(self):
        """
        :return: datetime: real current time, unless a historical time is set
        """
        if self._now:
            return self._now
        return datetime.datetime.utcnow().replace(tzinfo=utc)

class Lease(BaseLease):
    """
    Representation of a IPv4 dhcp lease
    Attributes:
        ip              The IPv4 address assigned by this lease as string
        hardware        The OSI physical layer used to request the lease (usually ethernet)
        ethernet        The ethernet address of this lease (MAC address)
        start           The start time of this lease as DateTime object
        end             The time this lease expires as DateTime object or None if this is an infinite lease
        hostname        The hostname for this lease if given by the client
        binding_state   The binding state as string ('active', 'free', 'abandoned', 'backup')
        data            Dict of all the info in the dhcpd.leases file for this lease
    """

    def __init__(self, ip, properties, **kwargs):
        super(Lease, self).__init__(ip, properties=properties, **kwargs)
        if 'starts' in properties:
            self.start = parse_time(properties['starts'])
        else:
            self.start = None
        if properties.get('ends', 'never') == 'never':
            self.end = None
        else:
            self.end = parse_time(properties['ends'])

        if 'hardware' in properties:
            self._hardware = properties['hardware'].split(' ')
            self.ethernet = self._hardware[1]
            self.hardware = self._hardware[0]
        else:
            self.hardware = None
            self.ethernet = None
        self.hostname = properties.get('client-hostname', '').replace("\"", "")

    @property
    def valid(self):
        """
        Checks if the lease is currently valid (not expired and not in the future)
        :return: bool: True if lease is valid
        """
        if self.end is None:
            if self.start is not None:
                return self.start <= self.now
            return True

        if self.start is not None:
            return self.start <= self.now <= self.end
        return self.now <= self.end

    def __repr__(self):
        return "<Lease {} for {} ({})>".format(self.ip, self.ethernet, self.hostname)

    def __eq__(self, other):
        return self.ip == other.ip and self.ethernet == other.ethernet and self.start == other.start


class Dhcp(object):
    """
    Class to parse isc-dhcp-server lease files into lease objects
    """

    regex_leaseblock = re.compile(
        r"lease (?P<ip>\d+\.\d+\.\d+\.\d+) {(?P<config>[\s\S]+?)\n}"
    )
    regex_leaseblock6 = re.compile(
        r"ia-(?P<type>ta|na|pd) \"(?P<id>[^\"\\]*(?:\\.[^\"\\]*)*)\" {(?P<config>[\s\S]+?)\n}"
    )
    regex_iaaddr = re.compile(
        r"ia(addr|prefix) (?P<ip>[0-9a-f:]+(/[0-9]+)?) {(?P<config>[\s\S]+?)\n\s+}"
    )

    def __init__(self, filename, now=None):
        check_datetime(now)

        self.filename = filename
        self.now = now

    def get(self, include_backups=False):
        """
        Parse the lease file and return a list of Lease instances.
        """
        leases = []
        with open(self.filename) as lease_file:
            lease_data = lease_file.read()
            for match in self.regex_leaseblock.finditer(lease_data):
                block = match.groupdict()

                properties, options, sets = _extract_properties(block["config"])
                if "hardware" not in properties and not include_backups:
                    # E.g. rows like {'binding': 'state abandoned', ...}
                    continue
                lease = Lease(
                    block["ip"],
                    properties=properties,
                    options=options,
                    sets=sets,
                    now=self.now,
                )
                leases.append(lease)

        return leases

    def get_current(self):
        """
        Parse the lease file and return a dict of active and valid Lease instances.
        The key for this dict is the ethernet address of the lease.
        """
        all_leases = self.get()
        leases = {}
        for lease in all_leases:
            if lease.valid and lease.active:
                leases[lease.ethernet] = lease
        return leases

    def get_history(self):
        """
        Parse the unique arptable
        """
        all_leases = self.get()
        leases = {}
        for lease in all_leases:
            #print(lease, lease.ethernet, lease.ip)
            #if lease.ip not in leases:
            leases[lease.ip] = lease.ethernet
            #else:

            #if lease.ethernet not in leases:
            #    leases[lease.ethernet] = lease.ip
        return leases


##aa = Dhcp("/var/lib/dhcp/dhcpd.leases")
#aa = Dhcp("/tmp/dhcpd.leases")
##al = aa.get_history()
#al = aa.get()
#leases = {}
##print(al, type(al))
#for lease in al:
#    print(lease, lease.ethernet, lease.ip)
#    leases[lease.ip] = lease.ethernet
#    #print(item,type(item),item.valid,item.ethernet,item.binding_state)
#print(leases)
##aa.get()
#print("--"*20)
#print(aa.get_current())
#print("--"*20)
#print(aa.get_history(),type(aa.get_history()))