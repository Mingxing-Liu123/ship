# -*-coding:utf-8-*-
"""tcp客户端"""
import socket
import time

def main():
    # 创建一个客户端套接字
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp_client.connect(('127.0.0.1', 6378))
    tcp_client.connect(('8.129.210.67',6378))
    lat = 23.15780224182429
    lon = 113.3408096369781
    for index in range(3):
        time.sleep(2)
        msg = '$,3,1,'
        lat = lat - 0.000151
        lon = lon + 0.000151
        msg += (str(lat))[0:10]
        msg += ','
        msg += (str(lon))[0:11]
        msg += ',*'
        sendmsg = msg.encode('ascii')
        print(sendmsg)
        tcp_client.send(sendmsg)
    while True:
        recv_data = tcp_client.recv(1024).decode('utf-8')  # .decode('utf-8')       # b'xxxx'
        print(recv_data)
    tcp_client.close()


if __name__ == '__main__':
    main()




