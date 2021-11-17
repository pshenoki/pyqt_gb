""" прикрепляю только лаунчер, если нужно могу подгрузить все файлы проекта"""
"""Лаунчер"""
import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие:\n '
                   'q - выход,\n '
                   's - запустить сервер и 2 клиента,\n '
                   'x - закрыть все окна, \n'
                   'clients:n - запустить сервер и указанное количество клиентов, вместо "n" выбрать число клиентов: ')

    if ACTION == 'q':
        break

    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client.py -n test1', creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client.py -n test2', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif 'clients' in ACTION:
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        client_num = int(ACTION.split(':')[1])
        for i in range(client_num):
            PROCESS.append(subprocess.Popen(f'python client.py -n test{i+1}',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
