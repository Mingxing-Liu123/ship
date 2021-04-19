#!/usr/bin/python

import uan_common
import os

class ConstHeader:

    def __init__(self):
        #super(ConstHeader, self).__init__()
        self.m_methodType = uan_common.kReply    # if reply, then don't other reply
        self.m_dataType   = uan_common.kOnlineNodes
        self.m_sendID     = 65535
        self.m_recvNodesNum    = 0
        self.m_sendFileNameLen = 0   # the length of sended file
        self.m_sendContentLen  = 0

    def toByte(self):
        res = bytes()
        for checkHeader in uan_common.kCheckHeaderArray:
            res += checkHeader.to_bytes(length = 1, byteorder = "big")

        res += self.m_methodType.encode(encoding = "utf-8")
        res += self.m_dataType.encode(encoding = "utf-8")
        res += self.m_sendID.to_bytes(length = 2, byteorder = "big")
        res += self.m_recvNodesNum.to_bytes(length = 1, byteorder = "big")
        res += self.m_sendFileNameLen.to_bytes(length = 1, byteorder = "big")
        res += self.m_sendContentLen.to_bytes(length = 4, byteorder = "big")

        return res

    

class VarHeader:
    def __init__(self):
        #super(VarHeader, self).__init__()
        self.m_nodeList = []
        self.m_fileName = ""

    def setNodeList(self, nodeList = []):
        self.m_nodeList = nodeList

    def setFileName(self, fileName = ""):
        self.m_fileName = fileName

    def toByte(self):
        res = bytes()
        for i in self.m_nodeList:
            res += i.to_bytes(length = 2, byteorder = "big")
        #print("fileName.type: ", self.m_fileName)
        res += self.m_fileName.encode(encoding = "utf-8")
        
        return res

class UAN_Packet:
    def __init__(self):
        self.m_cheader = ConstHeader()
        self.m_vheader = VarHeader()
        self.m_cmdStr = ""
        self.m_file = "" # filePath + fileName

    def setCmd(self, cmd = ""):
        #print("cmd" , cmd)
        self.m_cheader.m_sendFileNameLen = 0
        self.m_cheader.m_sendContentLen = len(cmd)
        self.m_vheader.m_fileName = ""  
        self.m_cmdStr = cmd

    def setFile(self, filePath, fileName):
        self.m_file = filePath
        if filePath[-1] != '/':
            self.m_file += '/'
        self.m_file += fileName
        fileLen = 0
        try:
            fileLen = os.path.getsize(self.m_file)
        except Exception as e:
            return -1

        self.m_cheader.m_sendFileNameLen = len(fileName)
        self.m_cheader.m_sendContentLen = fileLen
        self.m_vheader.m_fileName = fileName
        
        return 0
 

    def setRecvNodes(self, nodeList = []):
        self.m_cheader.m_recvNodesNum = len(nodeList)
        self.m_vheader.m_nodeList = nodeList

    def toByte(self):
        res = bytes()
        res += self.m_cheader.toByte()
        # print("const header.size: ", res)
        res += self.m_vheader.toByte()
        # print("var header.size: ", res)
        if self.m_cheader.m_sendFileNameLen == 0:
            res += self.m_cmdStr.encode(encoding = "utf-8")
        # print("packet.size: ", len(res))
        return res

    def setMethodType(self, mt = uan_common.kReply):
        self.m_cheader.m_methodType = mt

    def setDataType(self, dt = uan_common.kOnlineNodes):
        self.m_cheader.m_dataType = dt
