"""
本文件主要存放异步通信函数，在与NS-3仿真平台通信的时候用，
"""

from __future__ import absolute_import
from celery import shared_task
import time

import requests
from .simulationResult import ConnectWithNS3
from .handlerDB import HandleSimulationParament
#List的长度至少为8
#client_update(LIST)这个函数的意义在于把传给此函数的列表，通过socket通信发送到服务器。
@shared_task
def client_update(List = []):  #传进来十个个参数或者一个参数
    print(List)
    try:
        buff = ConnectWithNS3(List)
    except:
        print("can't connect with NS3")
        return "Error"
    else:
        pass

    RecvList = buff.split(";")  # buff == "Failed;PrimaryKey=123" or "Ok;..." or "Modem;mac1;mac2..."
    OnlineNodesList = []  #用来保存在线节点的MAC地址。
    resultSendToDjango={  #构造一个字典
        "ResultStatus":"Failed", #默认仿真结果状态为失败 :Ok,Failed,Online
        }
         
    if RecvList[0] == "Failed":  #仿真出错 "Failed;PrimaryKey=123" 
        resultSendToDjango["PrimaryKey"] = RecvList[1]  #只要传回primarykey就行。
        pk_str = RecvList[1].split("=")[1]
        pk = int(pk_str) #提取数据库的主键
        #table = 
    elif RecvList[0] == "Ok":  #仿真成功  “Ok;TimeDelay=123;PacketLoss=123;AverageThroughput=123;PrimaryKey=123”
        resultSendToDjango["ResultStatus"] = "Ok"
        resultlist=[]
        for i in range(1,5):
            kv = RecvList[i].split("=")
            k = kv[0] #key = keyvalue[0]
            v = kv[1]
            resultlist.append(v)
            resultSendToDjango.update({k:v})
        #print(resultlist)
        print("----------------")
        print(List[8])
        handleSimulationParament = HandleSimulationParament()
        handleSimulationParament.saveSimulationResults()
        SaveResultToDataTable(resultlist,List[8])
        

    elif RecvList[0] == "Modem":   #如果我查询的是在线节点数量，它返回"Modem;00:00:00:00:00:01;" 
        OnlineNodesList=RecvList[1:len(RecvList)]
    else:
        pass

    return OnlineNodesList  #返回一个列表，用于查询

"""
这个函数旨在把仿真参数表发给NS3启动进程，并根据仿真结果失败与否执行数据
"""
@shared_task
def StartSimulation(List = []):
    print(List)
    try:
        buff = ConnectWithNS3(List)
    except:
        print("can't connect with NS3")
        return "Error"
    else:
        pass


from .djangoToNS3 import connectWithNS3Directly
"""
*连接NS-3，获取在线节点的数量,如果成功则返回在线节点列表
如果获取失败,则返回false
"""
@shared_task
def Get_Oline_Nodes():
    try:
        Result_Str = connectWithNS3Directly("ModemRequest") # 成功联系了之后，会返回 Modem;mac1;mac2;mac3……
    except:
        print("can't connect with NS3")
        return "Error"
    else:
        if len(Result_Str)<1 and Result_Str[0] == "F":#请求失败
            return False
        MAC_List = Result_Str.split(";")[1:] #去除modem
        return MAC_List
"""

"""
#-----------------------------硬件仿真所用函数--------------------------------------#
"""
获取某个节点采集的数据,因为NS-3仿真平台没有数据库，因此该平台与节点之间的通信标准就是MAC地址
返回 Success;PH;TEMPREATUE;press;IPv4
"""
@shared_task
def Get_A_Node_Collect_Date(MAC_str): #MAC地址为MAC_str的节点的信息
    try:
        Result_Str = connectWithNS3Directly("ANodeStatus;"+MAC_str)
        return Result_Str
        if Result_Str[0] == "F":#获取信息失败
            return Result_Str
        #成功；“success;ph;temprature;press;ipv4”
        MSG_List = Result_Str.split(";")[1:]
        return MSG_List
    except e:
        return "Failed. Exception" + e