import multiprocessing
import socket
from copy import deepcopy


def send_message(conn,  conn_list, q):
    line = 'Сообщение отправлено'
    while True:
        if not q.empty():
            conn_list.append(q.get(block=False))
        data = conn.recv(1024)
        print(conn_list)
        for conn2 in conn_list:
            if conn2 != conn:
                conn2.send(data)
            else:
                conn.send(bytearray(line.encode('UTF-8')))

        # if time == 50000:
        #     conn.close()
        #     break

if __name__ == '__main__':
    sock = socket.socket()
    sock.bind(('localhost', 9090))  # к одному сокету может подключиться сколько угодно клинетов
    sock.listen()
    conn_list = []
    q = multiprocessing.Queue()
    while True:
        conn, addr = sock.accept() # вечно ожидается подключение
        print(f'connected: {addr}')
        conn_list.append(conn)
        print(conn_list)
        q.put_nowait(conn) #кладу в очередь сокет - а он изменяется
        for i in range(10):
            continue
        proc = multiprocessing.Process(target=send_message, args=( conn,  conn_list, q))
        proc.start()