#!/usr/bin/python
import uan_protocol
import uan_common

# is a singleton
class UAN_Recv:
    _instance = None
    _initFlag = False

    def __new__(cls, fd):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, socketFd):
        if self._initFlag == False:
            self._initFlag = True
            self.m_fd = socketFd
            self.m_que = []

    def setFd(self, socketFd):
        self.m_fd = socketFd

    def getQueLen(self):
        return len(self.m_que)

    def pushBack(self, recvStr = bytes()):
        self.m_que += recvStr #

    def getNBytes(self, nBytes = 0):
        res = bytes()
        if nBytes <= len(self.m_que):
            res = self.m_que[0 : nBytes]
            self.m_que = self.m_que[nBytes:]
        return res


recvQue = UAN_Recv(123)

"""
This class is not disigned for business level 
"""

class ConstHeaderManager:
    _instance = None
    _initFlag = False

    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initFlag == False:
            self._initFlag = True
            self.m_fdMap = {}
    
    def isFinished(self, fd = 0):
        if fd in self.m_fdMap:
            return True
        return False

    def eraseFd(self, fd = 0):
        if fd in self.m_fdMap:
            self.m_fdMap.pop(fd)

    def isValidCheckHeader(self, checkHeaderStr):
        if len(checkHeaderStr) < uan_common.kCheckHeaderLen:
            return False
        for checkIndex in range(0, uan_common.kCheckHeaderLen):
            if checkHeaderStr[checkIndex] != uan_common.kCheckHeaderArray[checkIndex]:
                return False
        return True

    def push(self,fd = 0, strIn = bytes()):
        if len(strIn) < uan_common.kConstHeaderLen :
            return False
        if self.isFinished():
            return False
        if not self.isValidCheckHeader(strIn):
            return False

        cheader = uan_protocol.ConstHeader()
        cheader.m_methodType = strIn[4]
        cheader.m_dataType = strIn[5]
        cheader.m_sendID   = int.from_bytes(strIn[6: 8], byteorder = "big", signed = False)
        cheader.m_recvNodesNum = strIn[8]
        cheader.m_sendFileNameLen = strIn[9]
        cheader.m_sendContentLen = int.from_bytes(strIn[10:14], byteorder = "big",signed = True)

        self.m_fdMap[fd] = cheader

        # print("const header, recvNodId:",cheader.m_sendID, "m_recvNodesNum:",cheader.m_recvNodesNum)

        return True
    
    """
    
    """
    def getVarHeaderValue(self, fd):
        res = []
        if fd not in self.m_fdMap:
            return res
        res.insert(0, self.m_fdMap[fd].m_recvNodesNum)
        res.insert(1, self.m_fdMap[fd].m_sendFileNameLen)
        return res

    def getContentLen(self, fd):
        res = -1
        if fd not in self.m_fdMap:
            return res
        res = self.m_fdMap[fd].m_sendContentLen
        return res

    def getdatatype(self,fd):
        res = -1
        if fd not in self.m_fdMap:
            return res
        res = self.m_fdMap[fd].m_dataType
        return res

class VarHeaderManager:
    _instance  = None
    _initFlag = False
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initFlag == False:
            self.m_fdMap = {}

    def isFinished(self, fd = 0):
        if fd in self.m_fdMap:
            return True
        return False

    def eraseFd(self, fd):
        if fd in self.m_fdMap:
            self.m_fdMap.pop(fd)

    def push(self, fd, vhlist, strIn):
        if len(vhlist) < 2:
            print("vhList < 2")
            return False
      
        nodeNum = vhlist[0]
        fileLen = vhlist[1]
        
        if len(strIn) < 2* nodeNum + fileLen:
            print("strIn < x")
            return False

        vheader = uan_protocol.VarHeader()
        for ite in range(0, nodeNum):
            nodeID = int.from_bytes(strIn[ite*2: ite*2 + 2], byteorder = "big", signed = False)
            vheader.m_nodeList.append(nodeID)

        vheader.m_fileName = strIn[nodeNum*2 : nodeNum*2 + fileLen]
        self.m_fdMap[fd] = vheader
        
        return True

class ContentManager():
    _initFlag = False
    _instance = None
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initFlag == False:
            self.m_fdMap = {}
    
    def setFd(self, fd, contentLen = 0):
        self.m_fdMap[fd] = contentLen
    
    def eraseFd(self, fd):
        if fd in self.m_fdMap:
            self.m_fdMap.pop(fd)
        return True

    def hasFd(self, fd):
        if fd in self.m_fdMap:
            return True
        return False

    def isEnd(self, fd):
        if fd not in self.m_fdMap:
            return True

        if self.m_fdMap[fd] <= 0:
            return True
        
        return False

    def getContent(self, fd):
        res = bytes()
        if fd not in self.m_fdMap:
            return res

        restLen = self.m_fdMap[fd]
        dataLen = recvQue.getQueLen()
        nBytes = min(restLen, dataLen)

        res = recvQue.getNBytes(nBytes)
        self.m_fdMap[fd] -= nBytes

        return res

chManager = ConstHeaderManager()
vhManager = VarHeaderManager()
contentM = ContentManager()
