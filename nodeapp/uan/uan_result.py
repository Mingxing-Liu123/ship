#!/usr/bin/python3
import time
import threading
class UAN_Result:
    _instance = None
    _initFlag = False
    lock = threading.RLock()

    def __new__(cls):
        
        if cls._instance is None:
            cls.lock.acquire()
            if cls._instance is None:
                #print("construct UAN_Result")
                cls._instance = super().__new__(cls)
            cls.lock.release()
        return cls._instance

    def __init__(self):
        if self._initFlag == False:
            self._initFlag = True
            self.m_taskIdMap = {}

    def isFinished(self, taskId):
        if taskId in self.m_taskIdMap:
            return True
        return False

    def getTaskResult(self, taskId):
        bTaskId = taskId.encode(encoding="utf-8")
        
        isFinish = self.isFinished(bTaskId)
        print("resultLen:", self.m_taskIdMap)
        if isFinish:
            res = self.m_taskIdMap[bTaskId]
            self.m_taskIdMap.pop(bTaskId)
            return res
        else:
            print("taskId error, please input corrected taskId, isFinsh =",isFinish)
        return b''

    def pushTaskResult(self, taskId, result):
        self.m_taskIdMap[taskId] = result
        return True

recvResult = UAN_Result()

class UAN_Process:
    _instance = None
    _initFlag = False
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super.__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initFlag == False:
            self._initFlag = True
            self.m_isRuning = True

    def getStatus(self):
        return self.m_isRuning

    def stop(self):
        self.m_isRuning = False
