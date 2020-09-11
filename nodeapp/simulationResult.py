
"""
# 通过socket方式连接到NS3,
该函数的作用是，首次连接到NS3，就根据输入列表的大小，来发送相应指令。
发送完毕后，就立马等待，等NS3进程返回数据之后，退出并返回接收数据。
"""
from socket import *
def ConnectWithNS3(List = []):
    PORT = 9999
    HOST = "127.0.0.1"
    BUFFSIZE = 1024
    ADDR = (HOST,PORT)

    if len(List) > 8:  #给ns3传送参数指令 有九个参数
        MSG="StartEmulation;--recvMAC="+List[0]+";"+"--sendMAC="+List[1]+";"
        MSG+=" --Modulation="+List[2] + " --MAC_Protocol="+List[3]
        MSG+=" --Routing_protocol="+List[4]+" --Transport="+List[5]
        MSG+=" --Application="+List[6]+" --Simulation_method="+List[7]
        MSG+=";--PrimaryKey="+str(List[8])
    else: #查询有多少节点在线
        MSG="ModemRequest"

    tcpCliSock = socket(AF_INET,SOCK_STREAM,0)
    tcpCliSock.connect(ADDR)

    tcpCliSock.send(MSG.encode()) #立刻发送指令
    #接收过程
    result_buff = tcpCliSock.recv(BUFFSIZE)
    tcpCliSock.close()
    buff = result_buff.decode("utf-8") #解码
    return buff