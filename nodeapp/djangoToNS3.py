#!/usr/bin/python3
#本文件存放的内容为django与NS3的信息交互

# 第一版数据构成
"""
根据仿真参数列表的大小，将参数列表字符串化，该函数是为了兼容socket通信部分
"""
def ns3ParamListToStr(ns3Param = []):
    size = len(ns3Param)
    ns3Message = ""
    if size == 0 :   #查看有多少个节点在线,只需要返回Modem;mac1;mac2……
        ns3Message = "ModemRequest"
    elif size == 1 :  #查看所有节点收集到的信息 
        ns3Message = "AllNodesDates"
    elif size == 2: # 查看逻辑上第paraments[0]个节点，且MAC地址为paraments[1]的节点的信息
        ns3Message = "A Node;" + str(ns3Param[0]) + ";" + ns3Param[1] 
    elif size == 9:  #给ns3传送参数指令 有九个参数
        ns3Message="StartEmulation;--recvMAC="+ns3Param[0]+";"+"--sendMAC="+ns3Param[1]+";"
        ns3Message+=" --Modulation="+ns3Param[2] + " --MAC_Protocol="+ns3Param[3]
        ns3Message+=" --Routing_protocol="+ns3Param[4]+" --Transport="+ns3Param[5]
        ns3Message+=" --Application="+ns3Param[6]+" --Simulation_method="+ns3Param[7]
        ns3Message+=";--PrimaryKey="+str(ns3Param[8])    

    return ns3Message 
"""
NS-3仿真平台返回给django的仿真结果，列表化
"""
def resultStrToNs3ParamList(ResultStr):
    if len(ResultStr) < 1:
        return []
    Result_List  = ResultStr.split(";")[1:]
    return Result_List


#1，兼容旧版本，用socket连接NS3
"""
def connectWithNS3Directly(date_str,Hard_Emul = False):
默认执行软件仿真，因此只需要发送一次就行，

"""
from socket import *

def connectWithNS3Directly(date_str,Node_MSG = False):
    PORT = 9999
    HOST = "127.0.0.1"
    BUFFSIZE = 1024
    ADDR = (HOST,PORT)

    tcpCliSock = socket(AF_INET,SOCK_STREAM,0)
    tcpCliSock.connect(ADDR)
    
    tcpCliSock.send(date_str.encode("utf-8")) #立刻发送指令
    
    #接收过程
    result_buff = tcpCliSock.recv(BUFFSIZE)

    tcpCliSock.close()
    buff = result_buff.decode("utf-8") #解码
    return buff

