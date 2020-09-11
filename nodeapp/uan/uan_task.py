#!/usr/bin/python
#----------------------------------
# uan_task.py
# author: chuanlong zhang
# time:   2019-10-28
#----------------------------------

import uan_recvQue
import uan_result #import recvResult

class Web_Task:
    def __init__(self, fd):
        self.m_fd = fd

    def run(self):
        content1 = [] 
        while not uan_recvQue.contentM.isEnd(self.m_fd):
            nBytes = uan_recvQue.contentM.getContent(self.m_fd) # return list
            content1 += nBytes

        content = bytes()
        for idx in content1:
            content += idx.to_bytes(length = 1, byteorder = "big")
        print("转换为字节:",content,type(content))
        b1 = b';'
        nIndex = content.find(b1)
        
        if nIndex >= 0:
            task = content[0: nIndex] # it don't contain the ''
            print("task",task)
            idIndex = task.find(b':')
            print("idindex:",idIndex)
            if idIndex >= 0:
                taskName = task[0:idIndex ] # it don't contain the ':'
                taskId = task[idIndex + 1 :]
                if taskName == b'taskId':

                    result = uan_result.UAN_Result()
                    
                    result.pushTaskResult(taskId, content[nIndex+1:])
                    print("data:", content[nIndex + 1:])

