# -*-coding:utf-8-*-
from  .ship_recvTread import serthread #, ship_RecvThread
from .ship_recvadmin import ship_RecvManager
from .ship_recQue import shiprecvQue
import time

class tcp_serlisen:
    _instance = None
    _initFlag = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ip="127.0.0.1", port=8080):
        if self._initFlag == False:
            self._initFlag = True
            self.m_port = port
            self.m_ip = ip
            self.m_fd = -1
            self.start()

    def start(self):
        r = serthread(self.m_port)
        # rm = ship_RecvManager()
        r.start()
        # rm.start()

    def sendtocli(self,msg = '',cli = None):
        self.m_fd = shiprecvQue.fdmap[cli]
        if self.m_fd == -1:
            return False
        self.m_fd.send(msg.encode())
        return True