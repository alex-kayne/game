import threading
import socket
from copy import deepcopy

sock = socket.socket()
sock.bind(('localhost', 9090))  # к одному сокету может подключиться сколько угодно клинетов
sock.listen()
conn_list = []
def send_message(conn, addr, conn_list):
    time = 0
    line = 'Сообщение отправлено'
    while True:
        time += 1
        print('connected')
        data = conn.recv(1024)
        print(data)
        print(conn)
        print(conn_list)
        for conn2 in conn_list:
            print(conn2 != conn)
            if conn2 != conn:
                conn2.send(data)
            else:
                conn2.send(bytearray(line.encode('UTF-8')))

        # if time == 50000:
        #     conn.close()
        #     break


while True:
    conn, addr = sock.accept() # вечно ожидается подключение
    conn_list.append(conn)
    thread = threading.Thread(target=send_message, args=(conn, addr, conn_list,))
    thread.start()
