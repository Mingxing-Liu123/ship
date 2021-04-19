#!/usr/bin/python3

#-------------------------
# uan_recvThread.py
#-------------------------

import socket
import threading
from uan_recvQue import recvQue

class RecvThread(threading.Thread):
    def __init__(self, fd):
        threading.Thread.__init__(self)
        self.m_fd = fd

    def run(self):
        while True:
            if self.m_fd == -1:
                print("fd is error")
                return
            # print("block the thread for TCP recv data:", self.m_fd)
            recvData = self.m_fd.recv(1024)
            print("接收到数据:", recvData,len(recvData))
            if not recvData:
                print("close the connection,fd=",self.m_fd)
                break
            recvQue.pushBack(recvData)

    
