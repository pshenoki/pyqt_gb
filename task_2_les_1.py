""" Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
    Меняться должен только последний октет каждого адреса.
    По результатам проверки должно выводиться соответствующее сообщение."""

import ipaddress
from task_1_les_1 import host_ping
IPV4 = '80.0.1.0/28'

subnet = ipaddress.ip_network(IPV4)
host_list = [str(host) for host in subnet.hosts()]

for tup in host_ping(host_list):
    print(f"{tup[0]} - {tup[1]}")
