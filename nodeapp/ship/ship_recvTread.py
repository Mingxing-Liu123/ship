# -*-coding:utf-8-*-
import threading
import socket
from  .ship_recQue import shiprecvQue
from .ship_result import ship_results
from ..handlerDB import saveshipdata
# 服务器监听线程
class serthread(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.m_port = port
        self.m_fd = -1

    def run(self):
        # 创建TCP套接字
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口复用
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口
        tcp_socket.bind(("", self.m_port))
        # 设置为被动监听状态，128表示最大连接数
        tcp_socket.listen(128)
        while True:
            # 等待客户端连接
            client_socket, ip_port = tcp_socket.accept()
            print("[新客户端]:", ip_port, "已连接")
            # 有客户端连接后，创建一个线程将客户端套接字，IP端口传入recv函数，
            t1 = threading.Thread(target=recv, args=(client_socket, ip_port))
            # 设置线程守护
            t1.setDaemon(True)
            # 启动线程
            t1.start()

#接收函数
def recv(client_socket, ip_port):
    flag =0
    datalen = 0
    cont = None
    while True:
        client_text = client_socket.recv(1024).decode('utf-8')
        # 如果接收的消息长度不为0，则将添加到消息队列并处理
        if client_text:
            print("[客户端消息]", ip_port, ":", client_text)
            data_list = delrest(list(client_text))
            # print("delrest:",data_list)
            datalen,cont = getdatalen(data_list)
            # print("datalen,cont:",datalen,cont,len(cont))
            if datalen > len(cont):
                print("数据不够")
                continue
            if len(cont) <= 0:
                continue
            if len(cont) < 6:
                flag = 0
                shiprecvQue.fdmap['other1'] = client_socket
                ship_results.otherdata = cont
                # print("0 fdmap:", shiprecvQue.fdmap)
                print("other1:", ship_results.otherdata)
                continue
            if cont[0] == '$' and cont[5] == 'D':
                flag = 1
                shiprecvQue.fdmap['ship'] = client_socket
                # print("1 fdmap:",shiprecvQue.fdmap)
                parse_gphpd(cont,datalen)
                continue
            else:
                flag = 2
                shiprecvQue.fdmap['other2'] = client_socket
                ship_results.otherdata = cont
                # print("2 fdmap:", shiprecvQue.fdmap)
                print("other2:", ship_results.otherdata)
                continue
        # 当客户端断开连接时，会一直发送''空字符串，所以长度为0已下线
        else:
            if flag == 0:
                shiprecvQue.fdmap['other1'] = -1
            elif flag == 1:
                shiprecvQue.fdmap['ship'] = -1
            else:
                shiprecvQue.fdmap['other2'] = -1
            print("客户端", ip_port, "已下线")
            # print("fd字典：",shiprecvQue.fdmap)
            client_socket.close()
            break
#删除上个数据包不完整的部分
def delrest(datalist = None):
    dlist = datalist.copy()
    indexlist = []
    cont = []
    for i in range(len(dlist)):
        if dlist[i] == '$':
            indexlist.append(i)
    # print("indexlist:",indexlist)
    if len(indexlist) == 0:
        return  cont
    for i in range(len(indexlist)):
        if indexlist[i] >= 4:
            cont = dlist[indexlist[i]-4:]
            # print("cont1:",cont)
            return cont
    # print("cont2:", cont)
    return cont

#解析数据,若累计接收多个数据包，只取第一个，会造成丢包
def parse_gphpd(contentlist,datalen):
    contentlist = contentlist[7:datalen]
    arg = {}
    i = 0
    preindex = 0
    for index in range(len(contentlist)):
        if contentlist[index] == ',':
            arg[i] = contentlist[preindex:index]
            preindex = index + 1
            i = i + 1
    arg[i] = str(contentlist[preindex:])
    processdata = [None]*20
    for index in range(len(arg) - 1):
        lt = arg[index]
        processdata[index] = float(''.join(lt))
    saveshipdata(processdata)
    print("recvadmin:",processdata)
#得到数据包的长度,这里只针对gphpd数据，只考虑长度在145-160之间的数据，
def getdatalen(data_list = None):
    datalen = int(0)
    cont = None
    if len(data_list) == 0:
        return datalen,cont
    lengthlist = data_list[0:2]
    if lengthlist[1] == ',':
        datalen = int(lengthlist[0])
        cont = data_list[2:]
        return datalen, cont
    else:
        lengthlist += data_list[2]
        if lengthlist[2] == ',':
            datalen = int(lengthlist[0]) * 10 + int(lengthlist[1])
            cont = data_list[3:]
            return datalen, cont
        else:
            datalen = int(lengthlist[0]) * 100 + int(lengthlist[1]) * 10 + int(lengthlist[2])
            cont = data_list[4:]
            shiprecvQue.getNBytes(1)
            return datalen, cont

def isvalid(lenlist = None):
    datalist = lenlist.copy()
    numberstr = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for index in range(len(lenlist)):
        if not lenlist[index]  in numberstr:
            return False
    return True