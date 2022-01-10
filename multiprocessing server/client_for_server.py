import socket
import multiprocessing



def recieve_msg(sock):
    while True:
        data = sock.recv(1024)
        print(data.decode('UTF-8'))



def send_message():
    while True:
        line = input()
        sock.send(bytearray(line.encode('UTF-8')))

if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    proc1 = multiprocessing.Process(target=recieve_msg, args=(sock,))
    proc1.start()
#    proc2 = multiprocessing.Process(target=send_message)

#    proc2.start()

    while True:
        line = input()
        sock.send(bytearray(line.encode('UTF-8')))

