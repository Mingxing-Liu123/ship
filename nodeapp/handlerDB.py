#本文件为数据库处理文件
"""
主要功能：增删查改
#增加 add
#删除 delete
#查找 find
#修改 modify
"""
#-----------------------------------------------------------老版数据库
from .models import SimulationParament
"""
删除数据表SimulationParament中某一行
"""
def deleteSimulationParament(pf):
	try:
		storeInfo = SimulationParament.objects.get(pk = pf)
	except:
		print("Can't find it")
		return False
	else:
		storeInfo.delete()
		return True


#-----------------------------------------------------------新版数据库

from .models import Net_Attribute,Time_Node, Raw_Node
from .models import MSG_PH_Attribute,MSG_Press_Attrubute,MSG_Temperature_Attribute
from .models import UanEmulation
#MAC属性，网络属性，水声节点熟悉，时刻节点属性，节点采集信息属性（PH，pressure,temperature）

"""------------------------------------------------------------------------
获取Raw_Node数据表中有多少个节点，并把节点序号输出来
"""
def getRawNodes(nodes = 5): #默认输出5个
    allData = Raw_Node.objects.all()
    minCount = min(nodes, allData.count())
    resultList = []
    for i in range(0,minCount):
        resultList.append(allData[i].RawNode_ID)
    return resultList

from .models import SimulationParament, UanEmulation
#import .models
#通过primarykey寻找到数据表中的某一行，并把输入列表存放到数据表当中,最后要把保存到数据表的主键提取出来 
class HandleSimulationParament:
    def __init__(self):
        self.m_SPTable = SimulationParament()
    
    def saveSimulationParaments(self, SimulationParams = []):
        if len(SimulationParams) < 10:
            return -1

        self.m_SPTable.RecvNodeMac = SimulationParams[0]
        self.m_SPTable.SendNodeMac = SimulationParams[1]
        self.m_SPTable.Modulation = SimulationParams[2]
        self.m_SPTable.MACPtorocols = SimulationParams[3]

        self.m_SPTable.Route = SimulationParams[4]
        self.m_SPTable.Transport = SimulationParams[5]
        self.m_SPTable.Application = SimulationParams[6]
        self.m_SPTable.Simulation = SimulationParams[7]
        self.m_SPTable.SimulationUser = SimulationParams[8]
        self.m_SPTable.TestName = SimulationParams[9]

        self.m_SPTable.save()
        return self.m_SPTable.id
    
    def saveSimulationResults(self, simulationResult, primaryKey):
        if len(simulationResult) < 4:
            return False
        try:
            self.m_SPTable = SimulationParament.objects.get(id = primaryKey)
        except:
            return False

        self.m_SPTable.Delay = simulationResult[0]
        self.m_SPTable.PacketLoss = simulationResult[1]
        self.m_SPTable.AverageThroughput = simulationResult[3]
        self.m_SPTable.save()
        return True

class RawNodeHandler:
    def isExist(nodeId):
        try:
            Raw_Node.objects.get(RawNode_ID = nodeId)
        except Exception as e:
            # the nodeId is not exist
            return False
        return True
    
    def createRawNode(nodeId, geoAddress = "None", macAddress = "00:00:00:00:00:00"):
        try:
            nodeNote = Raw_Node.objects.get(RawNode_ID = nodeId)
            nodeNote.Geo_Address = geoAddress
            nodeNote.MAC_Address = macAddress
        except Exception as e:
            newNode = Raw_Node()
            newNode.RawNode_ID = nodeId
            newNode.Geo_Address = geoAddress
            newNode.MAC_Address = macAddress
            newNode.save()

class UanEmulationDBHandler:
    def saveParamBeforeEmulated(taskId, user, srcFilePath, srcNodeId, emuNodeIds):
        uanEmulationTable = UanEmulation() 
        uanEmulationTable.taskID = taskId
        uanEmulationTable.emuUser = user
        uanEmulationTable.srcFilePath = srcFilePath
        
        if not RawNodeHandler.isExist(srcNodeId):
            RawNodeHandler.createRawNode(srcNodeId)
      
        uanEmulationTable.srcNodeID = Raw_Node.objects.get(RawNode_ID = srcNodeId)
        uanEmulationTable.save()
            
    def saveResultAfterEmulated(taskId, emuFilesPath):
        try:
            uanEmulationTable = UanEmulation.objects.get(taskID = taskId)
            uanEmulationTable.emuFilesPath = emuFilesPath
            uanEmulationTable.save()
        except Exception as e:
            print("exception,", e)
            return False
        return True

    def deleteParam(primaryKey):
        try:
            deletedParam = UanEmulation.objects.get(id = primaryKey)
            deletedParam.delete()
        except:
            return False
        return True

    def selectQuery(taskId):
        pass
        #uanEmulationTable.objects.get(taskID = taskId)
   
    def getSrcFilePath(primaryKey):
        try:
            uanEmulationTable = UanEmulation.objects.get(id = primaryKey)
            return uanEmulationTable.srcFilePath
        except Exception as e:
            print(e)
            return ""

    def getEmuResultFilePath(primaryKey):
        try:
            uanEmulationTable = UanEmulation.objects.get(id = primaryKey)
            return uanEmulationTable.emuFilesPath
        except Exception as e:
            print("can't get UanEmulation's object, id = ", primaryKey, e)
        return ""
    def getEmuTaskId(primaryKey):
        try:
            uanEmulationTable = UanEmulation.objects.get(id = primaryKey)

            return uanEmulationTable.taskID
        except Exception as e:
            print("can't get uanEmulation's object, id:",primaryKey)
            return ""

from .models import Ship_msg
#将实时获取的数据保存到(Ship_ID=1)的Ship_msg中
def saveshipdata(processdata = []):
    node = Ship_msg.objects.get(Ship_ID=1)
    node.heading = processdata[2]
    node.pitch = processdata[3]
    node.roll = processdata[4]
    node.poi_lat = processdata[5]
    node.poi_lng = processdata[6]
    node.alt = processdata[7]
    node.ve = processdata[11]
    node.vn = processdata[12]
    node.vu = processdata[13]
    node.save()

from .ship import wgs84_bd
def getshippoision():
    node = Ship_msg.objects.get(Ship_ID=1)
    poilist = []
    convertpoi = [None]*2
    poilist.append(float(node.poi_lat))
    poilist.append(float(node.poi_lng))
    # print("转换前的坐标：",poilist)
    convertpoi[0],convertpoi[1] = wgs84_bd.wgs84_bd09(poilist[0],poilist[1])
    # print("转换后的坐标:", convertpoi)
    return convertpoi

def getshipmsg():
    node = Ship_msg.objects.get(Ship_ID=1)
    poilist = []
    poilist.append(node.heading)
    poilist.append(node.pitch)
    poilist.append(node.roll)
    lat,lon = wgs84_bd.wgs84_bd09(float(node.poi_lat),float(node.poi_lng))
    poilist.append(lat)
    poilist.append(lon)
    poilist.append(node.alt)
    poilist.append(node.ve)
    poilist.append(node.vn)
    poilist.append(node.vu)
    return poilist