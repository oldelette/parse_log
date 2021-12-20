from dhcpleases import Dhcp
from atftp import Parser

lease = Dhcp("/var/lib/dhcp/dhcpd.leases")
dhcp_dic = lease.get_history()
tmp_dic = lease.get_current()
print(tmp_dic)
#print(lease.get_history(),type(lease.get_history()))

for key,val in dhcp_dic.items():
    print(key,val)

atftp_state = Parser("/var/log/atftpd.log")
res = atftp_state.fliter_service()
for item in res:
    print(item)



def check_sent_or_not():
    pass
