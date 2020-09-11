# -*-coding:utf-8-*-
class shipRecvQue:
    _instance = None
    _initFlag = False

    def __new__(cls, fd):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, socketFd):
        if self._initFlag == False:
            self._initFlag = True
            self.m_fd = -1
            self.m_que = []
            self.fdmap = {'ship':-1,'other1':-1,'other2':-1 }

    def getQueLen(self):
        return len(self.m_que)

#删除头部多余的信息
    def delrest(self):
        numberstr = ['1','2','3','4','5','6','7','8','9']
        while True:
            if len(self.m_que) <= 0:
                return
            if not self.m_que[0] in numberstr:
                self.getNBytes(1)
                continue
            else:
                break

    def getNBytes(self, nBytes = 0):
        res = bytes()
        if nBytes <= len(self.m_que):
            res = self.m_que[0 : nBytes]
            self.m_que = self.m_que[nBytes:]
        return res

shiprecvQue = shipRecvQue(123)