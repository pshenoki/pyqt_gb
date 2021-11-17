""" Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
  Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
  В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
  («Узел доступен», «Узел недоступен»).
  При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address()."""

import ipaddress
import subprocess
from subprocess import Popen
from threading import Thread

HOSTS_LIST = ['178.248.232.209', '11.11.11.123', "8.8.8.8", "1.1.1.1", "1.2.3.45", "bad_ip_address"]


def host_ping(host_list: list):
    return_list = []

    def is_valid(ip):
        with Popen(['ping', ip], creationflags=subprocess.CREATE_NEW_CONSOLE) as p:
            p.wait()
            if p.poll():
                return_list.append((ip, 'узел недоступен'))
            else:
                return_list.append((ip, 'узел доступен'))

    threads = []
    for host_name in host_list:
        try:
            ipv4 = str(ipaddress.ip_address(host_name))
            t = Thread(target=is_valid, args=(ipv4,))
            t.daemon = False
            t.start()
            threads.append(t)
        except ValueError:
            return_list.append((host_name, 'не существует данный IP'))

    for thread in threads:
        thread.join()

    return return_list


if __name__ == '__main__':
    for tup in host_ping(HOSTS_LIST):
        print(f"{tup[0]} - {tup[1]}")
