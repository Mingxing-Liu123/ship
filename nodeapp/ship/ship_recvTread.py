# -*-coding:utf-8-*-
import threading
import socket
from nodeapp.ship.ship_recQue import shipRecvQue
from ..handlerDB import  saveshipdata,saveshippos
from ..handlerFile import saveonlinnodes,delnode,get_from_file_nodes
# from ..models import Ship_msg
# # 服务器监听线程
#服务器监听线程
class serthread(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.m_port = port

    def run(self):
        # 创建TCP套接字
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口复用
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口
        tcp_socket.bind(("", self.m_port))
        # 设置为被动监听状态，128表示最大连接数
        tcp_socket.listen(128)
        print("开始监听")
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
    flag=False
    while True:
        client_text = client_socket.recv(150).decode('ascii')
        # 如果接收的消息长度不为0，则将添加到消息队列并处理
        if client_text:
            print("[客户端消息]", ip_port, ":", client_text)
            data_str = delrest(client_text)
            if data_str == None:
                continue
            nodeid = parse_pos(data_str)
            if not flag:
                flag=True
                saveonlinnodes(nodeid)
                shipRecvQue.get_instance().fdmap[nodeid] = client_socket
        # 当客户端断开连接时，会一直发送''空字符串，所以长度为0已下线
        else:
            flag=False
            shipRecvQue.get_instance().fdmap.pop(nodeid)
            delnode(nodeid)
            # print("删除onlinenode:",get_from_file_nodes())
            # print("删除fdmap：",recvque.fdmap)
            client_socket.close()
            print("客户端", ip_port, "已下线")
            break

def delrest(datastr = None):
    dstr = datastr
    s_pos = dstr.find('$')
    if s_pos == -1:
        return None
    dstr = dstr[s_pos:]
    e_pos = dstr.find('*')
    if e_pos == -1:
        return None
    else:
        return dstr[0:e_pos]

#解析数据 格式：$,nodeid,datatype,lat,lng,*
def parse_pos(data_str):
    d_str = data_str
    pos = d_str.find(',')
    d_str = d_str[pos+1:]
    pos = d_str.find(',')
    node_id = int(d_str[0:pos])
    d_str = d_str[pos+1:]
    pos = d_str.find(',')
    datatype=int(d_str[0:pos])
    d_str = d_str[pos + 1:]
    # 经纬度信息:
    if datatype==1:
        pos =d_str.find(',')
        lat = float(d_str[0:pos])
        d_str = d_str[pos + 1:]
        pos = d_str.find(',')
        lng = float(d_str[0:pos])
        plist = [None]*3
        plist[0] = node_id
        plist[1] = lat
        plist[2] = lng
        saveshippos(plist)
    # 通知信息:
    if datatype==2:
        pos =d_str.find(',')
        recvnodeid=int(d_str[0:pos])
        d_str = d_str[pos + 1:]
        pos =d_str.find(',')
        file_size=d_str[0:pos]
        d_str=d_str[pos+1:]
        pos =d_str.find(',')
        file_name=d_str[0:pos]
        msg="002,"+str(file_size)+','+str(file_name)
        res=shipRecvQue.get_instance().fdmap[recvnodeid].send(msg.encode())
        print("通知发送:",res,len(msg))
    return node_id