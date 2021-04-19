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
            self.datatype = None

    def isFinished(self, taskId):
        if taskId in self.m_taskIdMap:
            return True
        return False

    def getTaskResult(self, taskId):
        bTaskId = taskId.encode(encoding="utf-8")
        
        isFinish = self.isFinished(bTaskId)
        # print("result_taskid_map:", self.m_taskIdMap)
        if isFinish:
            res = self.m_taskIdMap[bTaskId]
            self.m_taskIdMap.pop(bTaskId)
            return res
        else:
            print("gettaskresult error",isFinish)
        return b''

    def getdatatype(self,taskId):
        bTaskId = taskId.encode(encoding="utf-8")
        # print("get taskidmap:",self.m_taskIdMap,bTaskId)
        isFinish = self.isFinished(bTaskId)
        # print("result_taskid_map:", self.m_taskIdMap)
        if isFinish:
            res = self.datatype
            # self.m_taskIdMap.pop(bTaskId)
            return res
        else:
            print("getdatatype error", isFinish)
        return b''


    def pushTaskResult(self, taskId, result,datatype):
        self.datatype = datatype
        self.m_taskIdMap[taskId] = result
        # print("push result taskidmap", self.m_taskIdMap)
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
