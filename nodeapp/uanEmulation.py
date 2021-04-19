#!/usr/bin/python3

from .uan import uan_client
import time

class UanNodeAdmin:
    _instance = None
    _initFlag = False
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initFlag == False:
            self._initFlag = True
            self.m_nodeID = []
            self.m_timeSpan = 60  # updata the nodeIDs per 60 seconds
            self.m_updataTime = 0

    def getOnlineNodes(self):
        # print("enter into getOnlineNodes",self.m_updataTime)
        currentTime = int(time.time())
        span = currentTime - self.m_updataTime
        if self.m_updataTime == 0 or span >= self.m_timeSpan:
            client = uan_client.UanSimulationClient()
            self.m_updataTime = int(time.time())
            resultBytes = client.getOnlineNodes()
            if len(resultBytes) != 0:
                resultStr = resultBytes.decode()

                print("onlinenode:", resultStr)
                nodeIdList = resultStr.split(",")
                nodeIdListInt = []
                try:
                    for node in nodeIdList:
                        nodeIdListInt.append(int(node))
                except Exception as e:
                    return []
                    print("exception:",e)
                nodeIdListInt.sort()
                self.m_nodeID = nodeIdListInt
        
        return self.m_nodeID
