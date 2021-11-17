""" Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
    Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
    (использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:"""

from task_1_les_1 import host_ping
from tabulate import tabulate
import ipaddress
from itertools import zip_longest

IPV4 = '80.0.1.0/28'
subnet = ipaddress.ip_network(IPV4)
host_list = [str(host) for host in subnet.hosts()]

'''Больше нравится такой вывод: '''
tuples_list = sorted(host_ping(host_list))
columns = ('ip address', 'response')
print(tabulate(tuples_list, headers=columns, tablefmt="grid"))


'''Но по условию нужно так... '''
correct_list = []
incorrect_list = []
for i in tuples_list:
    if i[1] == 'узел доступен':
        correct_list.append(i[0])
    if i[1] == 'узел недоступен':
        incorrect_list.append(i[0])

tup_list = zip_longest(correct_list, incorrect_list)
cols = ('Reachable', 'Unreachable')

print(tabulate(tup_list, headers=cols, tablefmt="grid"))
