"""
该文件主要处理上传及下载文件
"""

"""
把数据表SimulationParament中的主键为pf的数据写入到文件当中
"""
from .models import SimulationParament
def writeSimulationToFile(filename, pf):
    try:
        store_info = SimulationParament.objects.get(pk = pf)
    except:
        return False
    else:
        with open(filename,'w+') as fp:
            fp.write(str(store_info.SimulationUser)+str(" 设计的仿真参数\n"))
            fp.write(str("--------------------------------------------------------\n"))
            fp.write(str("发送节点MAC地址（Send Node MAC）      : ")+str(store_info.SendNodeMac) +str("\n"))
            fp.write(str("接收节点MAC地址（Recv Node MAC）      : ")+str(store_info.RecvNodeMac) +str("\n"))
            fp.write(str("调制方式（Modulation）    : ")+str(store_info.Modulation)+str("\n"))
            fp.write(str("MAC协议（MAC Protocol）   : ")+str(store_info.MACPtorocols)+str("\n"))

            fp.write(str("路由协议（Routing Protocol）  : ")+str(store_info.Route) +str("\n"))
            fp.write(str("传输层协议（Transport Protocol） : ")+str(store_info.Transport)+str("\n"))
            fp.write(str("应用层协议（Application Protocol）: ")+str(store_info.Application)+str("\n"))
            fp.write(str("仿真方式（Simulation Mode） : ")+str(store_info.Simulation) +str("\n"))
            fp.write(str("起始时间（Starting Time）: ")+str(store_info.RunningTime)+str("\n"))
            fp.write(str("--------------------------------------------------------\n"))
            fp.write(str("\n"))
            fp.write(str("本次实验结果\n"))
            fp.write(str("--------------------------------------------------------\n"))
            fp.write(str("丢包率（PacketLoss） : ")+str(store_info.PacketLoss) +str("%")+str("\n"))
            fp.write(str("延时（Delay）: ")+str(store_info.Delay)+str("ms")+str("\n"))
            fp.write(str("平均吞吐量（AverageThroughput） : ")+str(store_info.AverageThroughput)+str("Mbit/s")+str("\n"))
        return True
    
# ---------------------------
# 创建文件夹
# 参考 https://www.cnblogs.com/monsteryang/p/6574550.html
# --------------------------
def mkDir(dirPath):
    import os
    dirPath = dirPath.strip()
    dirPath = dirPath.rstrip('\\')
    
    isExists = os.path.exists(dirPath)
    if not isExists:
        os.makedirs(dirPath)
        print("create path successfully:", dirPath)

    return dirPath

# 配置文件
import json
class ConfigCenter:
    m_instance = None
    m_isCreated = False
    
    def __new__(cls):
        if cls.m_instance is None:
            cls.m_instance = super().__new__(cls)

        return cls.m_instance

    def __init__(self):
        if self.m_isCreated is False:
            self.m_isCreated = True
            self.m_nodeIDs = []
            self.m_nodeIDMap = {}
            self.m_resultDir = ""
            self.m_resultZipPath = ""
            self.readConfig() # init
            

    def readConfig(self):
        configContent = ""
        with open("config.txt",'rb') as fp:
            configContent = fp.read()

        configDict = json.loads(configContent)
        self.m_nodeIDs = configDict["nodeIDs"]

        for nodeID in self.m_nodeIDs:
            nodeIDstr = "nodeID" + str(nodeID)
            if nodeIDstr in configDict:
                self.m_nodeIDMap[nodeIDstr] = configDict[nodeIDstr] 

        self.m_resultDir = configDict["resultDir"]
        self.m_resultZipDir = configDict["resultZipDir"]

    def getNodeAccount(self, nodeIDint):
        resAccount = {}
        nodeIDstr = "nodeID" + str(nodeIDint)
        
        if nodeIDstr in self.m_nodeIDMap:
            resAccount["ipv4"] = self.m_nodeIDMap[nodeIDstr][0]
            resAccount["userName"] = self.m_nodeIDMap[nodeIDstr][1]
            resAccount["passWord"] = self.m_nodeIDMap[nodeIDstr][2]
        return resAccount

    def getServerAccount(self):
        return self.getNodeAccount(0)
    def getNodes(self):
        return self.m_nodeIDs
    def getResultDir(self):
        return self.m_resultDir
    def getResultZipDir(self):
        return self.m_resultZipDir

"""
上传文件，记录下来
"""
class saveUANEmulationResultToFile(object):
    def __init__(self, RequestFile, taskId, emuNodes):
        self.m_requestFile = RequestFile
        self.m_taskId = taskId
        self.m_emuNodes = emuNodes
        self.m_dir = ""
    def save(self):
        self.__setDir()
        self.__saveReadMe()
        ret = self. __saveUploadFile()
        return ret

    def __setDir(self):
        config = ConfigCenter()
        self.m_dir = config.getResultDir()
        
        if self.m_dir[-1] != '/':
            self.m_dir = self.m_dir + "/"
        self.m_dir = self.m_dir + self.m_taskId
        self.m_dir = mkDir(self.m_dir)
        
        if self.m_dir[-1] != '/':
            self.m_dir = self.m_dir + "/"

    def __saveReadMe(self):
        readMeName = self.m_dir + "readme.md"
        readMeContents = []
        readMeContents.append("# Uan Emulation\n")
        readMeContents.append("\n1. source file:" + self.m_requestFile.name)
        readMeContents.append("\n2. nodes\n")
        readMeContents.append("\n    1. sender node:" + str(self.m_emuNodes[0]))
        receiveNodes = ""
        for index in range(1, len(self.m_emuNodes)):
            receiveNodes = receiveNodes + ", " + str(self.m_emuNodes[index])
        readMeContents.append("\n    2. receiver node:" + receiveNodes)
        
        with open(readMeName, "w+") as f:
            for aLine in readMeContents:
                f.write(aLine)

    def __saveUploadFile(self):
        suffix = self.m_requestFile.name.split('.')[-1]
        fileNameBuff = self.m_taskId + "." + suffix
        fileName = self.m_dir + fileNameBuff

        with open(fileName,'wb') as fp:
            for chunk in self.m_requestFile.chunks():
                try:
                    fp.write(chunk)
                except Exception as e:
                    print("saveUploadFile exception,", e)
                    return "" # error
        return fileName

class UanResultZip(object):
    def __init__(self, taskId):
        self.m_taskId = taskId
        self.m_zipFilePath = ""
        self.__initClass()

    def hasZipFile(self):
        import os
        return os.path.exists(self.m_zipFilePath)

    def createZipFile(self):
        config = ConfigCenter()
        resultPath = config.getResultDir()
        if resultPath[-1] != '/':
            resultPath = resultPath + '/'
        resultPath = resultPath + self.m_taskId
        self.__makeZip(resultPath, self.m_zipFilePath)

        return self.m_zipFilePath
        
    def getZipFileDir(self):
        if self.hasZipFile():
            return self.m_zipFilePath
        return ""

    def __initClass(self):
        config = ConfigCenter()
        self.m_zipFilePath = config.getResultZipDir()
        if self.m_zipFilePath[-1] != '/':
            self.m_zipFilePath = self.m_zipFilePath + "/"
        self.m_zipFilePath = self.m_zipFilePath + self.m_taskId + ".zip"

    def __makeZip(self, sourceDir, outputFile):
        import os, zipfile
        zf = zipfile.ZipFile(outputFile, "w", zipfile.zlib.DEFLATED)
        for aFile in os.listdir(sourceDir):
            filePath = os.path.join(sourceDir, aFile)
            zf.write(filePath, aFile)
        zf.close()

