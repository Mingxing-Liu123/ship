#!/usr/bin/python3
#------------------------------------
# uan_client.py
#
#------------------------------------
import socket, time, uuid, threading
import uan_protocol, uan_send, uan_common, uan_result
from uan_recvAdmin import UAN_RecvManager as recvManager
from uan_recvThread import RecvThread

class UanSimulationClient:
    _initFlag = False
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
 
        return cls._instance
    
    def __init__(self, ip = "127.0.0.1", port = 8888):
        
        if self._initFlag == False:
            self.m_socket = -1
            self.m_ip = ip
            self.m_port = port

            res = self.connect()
            if not res:
                return

            self._initFlag = True
            self.start()
    

    def __del__(self):
        if self.m_socket != -1:
            self.m_socket.close()
    
    def uan_async(function):
        def createTaskThread(*args, **kwargs):
            th = threading.Thread(target = function, args = args, kwargs = kwargs)
            th.start()
        return createTaskThread


    def connect(self):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.m_socket.connect((self.m_ip, self.m_port))
        except Exception as e:
            self.m_socket.close()
            print("fail to connect server")
            return False
        return True

    def getTaskId(self):
        ymd = time.strftime("%Y%m%d", time.localtime())
        return ymd + "#" + str(uuid.uuid1())

    def start(self):                
        rh = RecvThread(self.m_socket) 
        r = recvManager(self.m_socket)
        
        rh.start()
        r.start()
    ## -------------------------    

    # get online nodes
    def getOnlineNodes(self):
        pt = uan_protocol.UAN_Packet()
        pt.setMethodType(uan_common.kRequest)
        pt.setDataType(uan_common.kOnlineNodes)

        taskId = self.getTaskId()
        pt.setCmd("taskId:"+taskId)

        uan_send.UAN_Send.send(fd = self.m_socket, packet = pt)
        
        onlineNodes = bytes()
        for x in range(0,3):
            # datatype = uan_result.recvResult.getdatatype(taskId)
            onlineNodes = uan_result.recvResult.getTaskResult(taskId)
            # print("---taskResult:",onlineNodes)
            if len(onlineNodes) != 0:
                # print("datatype:",datatype==0x22)
                return onlineNodes
            time.sleep(1) 
        # print("onlineslist:",onlineNodes)
        return onlineNodes

    #检查进度，最多5秒
    def checkprogress(self,taskId):
        pt = uan_protocol.UAN_Packet()
        pt.setMethodType(uan_common.kRequest)
        pt.setDataType(uan_common.Kcheckprogress)
        pt.setCmd("taskId:" + taskId)

        uan_send.UAN_Send.send(fd=self.m_socket, packet=pt)

        for x in range(0,5):
            datatype = uan_result.recvResult.getdatatype(taskId)
            connent = uan_result.recvResult.getTaskResult(taskId)
            # print("datatype,connent:", datatype,connent)
            if datatype != b'':
                print("datatype,connent:", datatype,connent)
                return datatype,connent
            time.sleep(1)
        return datatype,connent

    # get nodes MSG
    def getNodeMsg(self, nodeIdList = []):
        if len(nodeIdList) == 0:
            return ""
        pt = uan_protocol.UAN_Packet()
        pt.setMethodType(uan_common.kRequest)
        pt.setDataType(uan_common.kNodeMsg)
        pt.setRecvNodes(nodeIdList)
        taskId = self.getTaskId() # get task id
        pt.setCmd("taskId:"+taskId)
       
        uan_send.UAN_Send.send(fd = self.m_socket, packet = pt)

        nodesMsg = bytes()
        for x in range(0,3):
            datatype = uan_result.recvResult.getdatatype(taskId)
            nodesMsg = uan_result.recvResult.getTaskResult(taskId)
            if len(nodesMsg) != 0:
                break
            time.sleep(1) 
        # print("datatype:",datatype)
        return nodesMsg

    def __sendPacketForFileEmulated(self, nodeIdList, fileName, taskId):
        nodesLen = len(nodeIdList)
        minNumForEmulatedNodes = 2 # the min emulated nodes' number is 2
        if nodesLen < minNumForEmulatedNodes:
            return False
        pt = uan_protocol.UAN_Packet()
        pt.setMethodType(uan_common.kRequest)  # set 1
        pt.setDataType(uan_common.kOne2Many)   # set 2
        pt.setRecvNodes(nodeIdList)            # set 3
        pt.setCmd("taskId:" + taskId + ";"+"file:"+fileName) # set 4

        uan_send.UAN_Send.send(fd = self.m_socket, packet = pt)

        return True

    # get send files
    def getFileResult(self, nodeIdList, fileName, taskId):
        ret = self.__sendPacketForFileEmulated(nodeIdList, fileName, taskId)
        if ret == False:
            return False
        datatype = b''
        for x in range(0,5):
            datatype = uan_result.recvResult.getdatatype(taskId)
            content = uan_result.recvResult.getTaskResult(taskId)
            if datatype != b'':
                break
            time.sleep(1)
        if datatype == 0x50:
            print("启动成功")
            while True:
                stat,cont = self.checkprogress(taskId)
                if stat == 0x16:
                    print("p2p has finished:",cont)
                    index = cont.find(b':')
                    filepath = cont[index+1:]
                    # print("filepath:", filepath,type(filepath))
                    return filepath
                elif stat == 0x15:
                    continue
                else:
                    print("进度检查超时，stat:",stat)
                time.sleep(3)
        else:
            print("启动失败,datatype:",datatype)
            return  False

    @uan_async
    def async_getFileResult(self, nodeIdList, fileName, taskId, callback):
        # print("fileName:",fileName)
        fileResult = self.getFileResult(nodeIdList, fileName, taskId)
        print("filesResult:",fileResult)
        if fileResult == False:
            return False
        callback(taskId, fileResult)
        return True
