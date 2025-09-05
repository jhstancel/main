import nmap
import sys

nm_scan = nmap.PortScanner()
nm_scanner = nm_scan.scan('192.168.1.13', '80', arguments='-O')
print("The host is: ", nm_scanner['scan'], ['192.168.1.13'], ['status'], ['state'])

import nmap
import os
import sys


def get_arp():
    lines = str(os.system('arp -a')).splitlines()
    IPs = []
    for line in lines:
        if '.' in line:
            IPs.append(line.split()[0])

    return IPs


print(get_arp())

"""nm_scan = nmap.PortScanner()
nm_scanner = nm_scan.scan('192.168.1.13', '80', arguments='-O')

if 'scan' in nm_scanner and '192.168.1.13' in nm_scanner['scan']:
    host_info = nm_scanner['scan']['192.168.1.13']
    host_status = host_info['status']['state']

    print("The host is: ", host_status)
else:
    print("Host not found or scan results are not available.")"""

"""webster = {
    "fruit": "apple",
    "animal": "elephant",
    "color": "blue",
    "city": "New York",
    "flower": "rose"
}
print(webster["fruit"])"""
