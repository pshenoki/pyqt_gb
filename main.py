""" Написать класс Pinger, который будет раз в час пинговать заданные адреса и записывать в БД результаты пинга.

У класса должен быть атрибут списка пингуемых хостов (можно задавать при инициализации).
Методы добавления хоста в список пингуемых, а так же удаления. При добавлении предусмотреть валидации ip адреса,
добавлять только валидные адреса и домены.

В отдельном атрибуте должно хранится подключение к БД. Подключение создается при инициализации класса.

Отдельным методом сделать запуск работы класса на пингование.

Во время пингования класс проверяет актуальный список пингуемых адресов, пингует их и записывает результат
в БД.

Примерная структура БД:
id: UUID (первичный ключ, идентификатор записи в таблице)
host: str (пингуемый адрес)
ping_time: datetime (время пингования)
result: bool (True - если адрес доступен, False - если адрес не доступен)

В качестве БД использовать postgresql, ORM - sqlalchemy.
У класса предусмотреть метод для вывода результатов пинга из БД. На вход он должен принимать адрес хоста
и интервал времени за который нужно получить данные. Вывод сделать ввиде таблички где будет наглядно
показано время и доступность адреса.

Для пингования лучше использовать какую-нибудь python библиотеку. Я использовал aio_ping, работает хорошо.
Класс должен работать асинхронно."""

from sqlalchemy import create_engine
from datetime import datetime
from ipaddress import ip_address
from time import sleep
from subprocess import Popen
from threading import Thread
from tabulate import tabulate


class Pinger:
    time_sleep = 3600
    connection_params = "postgresql+psycopg2://user:123456@localhost/pinger"

    def __init__(self, name: str, host_set: set):
        self.name = name
        self.host_set = host_set
        self.conn = create_engine(self.connection_params).connect()

    def wait_hour(self):
        sleep(self.time_sleep)

    @staticmethod
    def is_valid_ip(ip):
        try:
            ip_address(ip)
            return True
        except ValueError:
            return False

    def insert_ip(self, ip):
        if self.is_valid_ip(ip):
            self.host_set.add(ip)
            print(f"{ip} - успешно добавлен")
        else:
            print(f"{ip} - не прошел провеку")

    def delete_ip(self, ip):
        if self.is_valid_ip(ip):
            self.host_set.remove(ip)
            print(f"{ip} - успешно удален")
        else:
            print(f"{ip} - не прошел провеку")

    def host_ping(self):
        return_list = []

        def check_connection(ip):
            with Popen(['ping', ip], stdout=False) as p:
                p.wait()
                if p.poll():
                    return_list.append((ip, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'False'))
                else:
                    return_list.append((ip, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'True'))

        threads = []
        for host_name in self.host_set:
            ipv4 = str(ip_address(host_name))
            t = Thread(target=check_connection, args=(ipv4,))
            t.daemon = False
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        return return_list

    def insert_in_database(self, data):
        self.conn.execute(f"insert into pinger_schema.ping_table (host, ping_time, result) values {str(data)[1:-1]}")

    def main_loop(self):
        #while True:
        ins_data = self.host_ping()
        self.insert_in_database(ins_data)
        #self.wait_hour()

    @staticmethod
    def table_view_format(values):
        columns = ("index", "host", "ping_time", "result")
        print(tabulate(values, headers=columns, tablefmt="grid"))

    def get_info(self, ip, date_start, date_end):
        values_ = self.conn.execute(
            f"select id, host, ping_time, result "
            f"from pinger_schema.ping_table "
            f"where host = '{ip}' "
            f"and ping_time between '{date_start}' and '{date_end}';"
            )
        tuples_list = [tuple(val) for val in values_]
        self.table_view_format(tuples_list)


if __name__ == "__main__":
    pi = Pinger('lol', {'178.248.232.209', '11.11.11.123', "8.8.8.8", "1.1.1.1", "1.2.3.45"})
    pi.main_loop()
    pi.get_info('178.248.232.209', '2021-11-18 22:57:08', '2021-11-18 23:11:11')
