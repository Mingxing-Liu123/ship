# -*-coding:utf-8-*-
"""tcp客户端"""
import socket
import time

def main():
    # 创建一个客户端套接字
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp_client.connect(('127.0.0.1', 8080))
    tcp_client.connect(('8.129.210.67',6378))
    testmsg = '1,2,3,4,5,6,7,8,9,'
    length = str(len(testmsg))
    sendtestmsg = (length + ',' + 'weq\r\n').encode('utf-8')
    # print(sendtestmsg)
    # tcp_client.send(sendtestmsg)
    msg2 = '56.122,-4920.200,56712.901,-288.918,0.004,0.024,-0.001,0.020,0.011,-0.019,1.808,15,15,4*60'
    lat = 23.15780224182429
    lon = 113.3408096369781
    for index in range(10):
        time.sleep(2)
        msg = '$GPHPD,1688,357049.190,66.61,-0.34,10.26,'
        lat = lat - 0.000151
        lon = lon + 0.000151
        msg += (str(lat))[0:10]
        msg += ','
        msg += (str(lon))[0:11]
        msg += ','
        for i in range(len(msg2)):
            msg += msg2[i]
        length = str(len(msg))
        # gphpdsendmsg = ('$' + length + ','+'178,$'+  '\r\n').encode('ascii')
        gphpdsendmsg = (msg + length + ',' + msg +'\r\n').encode('ascii')
        print(gphpdsendmsg)
        tcp_client.send(gphpdsendmsg)
    while True:
        recv_data = tcp_client.recv(1024).decode('utf-8')  # .decode('utf-8')       # b'xxxx'
        print(recv_data)
    tcp_client.close()


if __name__ == '__main__':
    main()




