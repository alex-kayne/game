import socket
import threading
sock = socket.socket()
sock.connect(('localhost', 9090))

def recieve_msg():
    while True:
        data = sock.recv(1024)
        print(data.decode('UTF-8'))

def send_message():
    while True:
        line = input()
        sock.send(bytearray(line.encode('UTF-8')))

thread1 = threading.Thread(target=recieve_msg)
thread2 = threading.Thread(target=send_message)
thread1.start()
thread2.start()


