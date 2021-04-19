#!/usr/bin/python
#-----------------------------------
# uan_recvAdmin.py
#-----------------------------------
import threading
import uan_recvQue,uan_common,uan_task
#from uan_result import UAN_Process

class UAN_RecvManager(threading.Thread):
    def __init__(self, fd):
        threading.Thread.__init__(self)
        #super(UAN_RecvManager, self).__init__()
        self.m_fd = fd
        return

    def run(self):
        if self.m_fd == -1:
            return 
        rQue = uan_recvQue.recvQue
        rQue.setFd(self.m_fd)
        datatype = None
        i = 0
        while True:
            if rQue.getQueLen() <= 0:
                continue

            if uan_recvQue.chManager.isFinished(self.m_fd):
                if i == 0:
                    print("has construct const Header,")
                    i = i + 1
                #print("has construct const header")
                if uan_recvQue.vhManager.isFinished(self.m_fd):
                    if i == 1:
                        print("has construct variable header")
                        i = i + 1
                    webTask = uan_task.Web_Task(self.m_fd)
                    webTask.run(datatype)
                    uan_recvQue.chManager.eraseFd(self.m_fd)
                    uan_recvQue.vhManager.eraseFd(self.m_fd)
                    uan_recvQue.contentM.eraseFd(self.m_fd)
                    print("handle a packet") 
                   # break

                else: # construct vheader
                    
                    length = rQue.getQueLen()
                    # print("varHeadlen:",length)
                    vhList = uan_recvQue.chManager.getVarHeaderValue(self.m_fd)
                    # print("vhlist:",vhList[0],vhList[1])
                    if len(vhList) >= 2:
                        varLen = vhList[0] * 2 + vhList[1]
                        if varLen <= length:
                            varData = rQue.getNBytes(varLen)
                            uan_recvQue.vhManager.push(self.m_fd, vhList, varData)
                        else:
                            print("vhList:",vhList[0], vhList[1])
                    else:
                        print("vhList.size<= 2,",len(vhList))
            else: # construct cheader
                length = rQue.getQueLen()
                # print("cheadlen:",length)
                if length >= uan_common.kConstHeaderLen:
                    chData = rQue.getNBytes(uan_common.kConstHeaderLen)
                    uan_recvQue.chManager.push(self.m_fd, chData)
                    contentLen = uan_recvQue.chManager.getContentLen(self.m_fd)
                    datatype = uan_recvQue.chManager.getdatatype(self.m_fd)
                    print("datatype:",datatype,type(datatype))
                    uan_recvQue.contentM.setFd(self.m_fd, contentLen)

