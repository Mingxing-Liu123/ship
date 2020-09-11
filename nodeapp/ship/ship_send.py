# -*-coding:utf-8-*-
from .Socket_tcp import tcp_serlisen
from .ship_common import *
from .ship_recQue import shiprecvQue
def sendlinetoship(poilist = []):
#一次发送10个点
    # msg = ''
    # msg += route_line
    # msg += ','
    # for index in range(len(poilist)):
    #     msg += poilist[index]
    #     msg += ','
    # msg = msg[:-1]
    # print(len(msg))
    # sendmsg = str(len(msg)) + ',' + msg
    # tcp_send = tcp_serlisen()
    # tcp_send.sendtocli(sendmsg)
    # print("发送的消息:",sendmsg,type(sendmsg))
#无人船只能一个一个坐标接收,所以需要发10次,分开发
    for index in range(int(len(poilist)/2)):
        msg = ''
        msg += route_line
        msg += ','
        msg += poilist[index*2]
        msg += ','
        msg +=  poilist[index*2 + 1]
        sendmsg = str(len(msg)) + ',' + msg
        tcp_send = tcp_serlisen()
        res = tcp_send.sendtocli(sendmsg,'ship')
    return res

def sendcomtoship():
    msg = ''
    msg += control
    msg += ','
    sendmsg = str(len(msg)) + ',' + msg
    tcp_send = tcp_serlisen()
    res = tcp_send.sendtocli(sendmsg,'ship')
    return res



