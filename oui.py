import urllib.request
import re


def ParseIEEEOui(url: str):
    # with urllib.request.urlopen(url) as response:
    #     data = response.read()
    # # print(data)
    IEEOUI = []
    for line in data.decode().split('\n'):
        try:
    	    mac, company = re.search(r'([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})\s+\(hex\)\s+(.+)', line).groups()
    	    IEEOUI.append(dict(mac=mac, company=company))
        except AttributeError:
            continue

    return IEEOUI

# sample = 'http://python.org/'
sample = 'https://standards-oui.ieee.org/oui/oui.txt'
res = ParseIEEEOui(sample)
print(res)
