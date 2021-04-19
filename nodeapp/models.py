from django.db import models
import datetime
from django.utils import timezone
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User  #从django中的模型导入用户模型。
#表明每个用户做仿真的时候所设置了参数，一个用户可能对应多个参数设置

#仿真参数
class SimulationParament(models.Model):
    #用户
    SimulationUser = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True) 

    #仿真参数
    TestName = models.CharField(max_length=100,help_text="the name of test")    #实验名称

    #7个不同的仿真参数
    #NumNode = models.IntegerField(help_text="仿真节点数量，The number of Nodes")  #仿真节点数量   
    RecvNodeMac = models.CharField(max_length=18,default="",help_text="接收消息节点的物理地址")
    SendNodeMac = models.CharField(max_length=18,default="",help_text="发送消息的节点物理地址")

    Modulation = models.CharField(max_length=10,help_text="调制方式，Modulation,QPSK,MFSK") #调制方式，QPSK,MFSK
    MACPtorocols = models.CharField(max_length=50,help_text="MAC层协议,for example,aloha protocol") # MAC层协议
    Route = models.CharField(max_length=50,help_text="路由协议,route protocols")     #路由协议   
    Transport = models.CharField(max_length=50,help_text="传输层协议,for instance,UDP")  #传输层协议
    Application = models.CharField(max_length=50,default="CBR",help_text="应用层协议,for instance,CBR") #应用层协议
    Simulation = models.CharField(max_length=50,help_text="硬件仿真还是软件仿真,simulation or emulation")  #硬件仿真还是软件仿真
    
    #仿真起始时间
    RunningTime = models.DateTimeField("仿真开始时间",default=timezone.now)

    #仿真结果
    PacketLoss = models.IntegerField(help_text="PacketLoss，丢包率",default=-1)
    Delay = models.IntegerField(help_text="delay ,延时",default=-1)
    AverageThroughput = models.IntegerField(help_text="AverageThroughput,平均吞吐量",default=-1)#怎么改为浮点型数，这是一个小问题
    class Meta:  
        ordering = ['-RunningTime']  #按照运行起点时间排序
        #permissions=((""),)

    def __str__(self):
        return self.TestName
    def get_absolute_url(self):
        return reverse("simulationparament_detail",args=[str(self.id)])
    


#项目负责人名单，即管理者,与用户无关
class Management(models.Model): #因为“adminstrator”可能存在与系统当中，故避开此词
    name=models.CharField(max_length=20,help_text="the name of administrator") #管理者名字
    job = models.CharField(max_length=50,help_text="job") #工作岗位
    call = models.CharField(max_length=11,help_text="the phone number") #电话
    email = models.EmailField(max_length=50,help_text="the email of manager") #email
    office_address=models.CharField(max_length=100,help_text="office address") #办公地址

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("management_detail",args=[str(self.id)])

"""
数据表构造思路图
|---------------------------------------------------------------|
|           节点MAC属性         |                  |             |
|           节点网络属性         |                  |             |
|           节点地理属性         |                  |             |
|------------------------------|                  |             |
| 节点PH值属性 |                 |   水声节点属性     |             |
| 节点温度属性 |  节点信息采集属性  |                  |             |
| 节点压强属性 |                 |                  |   时刻节点   |
|------------------------------|                  |             |
|        节点逻辑属性（节点ID）   |                  |              |
|-------------------------------------------------|             |
|                     时刻                         |             |
|---------------------------------------------------------------|

仿真数据表构造图
|--------------------|
| 发送节点（时刻节点）  |
| 接收节点（时刻节点）  |
| 发送文件            |
| 接收文件            |
|--------------------|

仿真结果计算数据表构造图
|
"""

class Net_Attribute(models.Model): #网络层属性
    Node_IPv4 = models.GenericIPAddressField(help_text = "Node IPv4 address")
    
    def __str__(self):
        return self.Node_IPv4
    
class MSG_PH_Attribute(models.Model): #采集信息属性_ph value
    Node_PH = models.DecimalField(max_digits=3,decimal_places=1,default = 7.0,help_text="PH value, such as 7.00，12.01")
    
    def __str__(self):
        return str(self.Node_PH)

class MSG_Temperature_Attribute(models.Model): # temperature
    Node_Temperature = models.DecimalField(max_digits=4,decimal_places=1,default = 20.0,help_text = "Temperature , such as 37.0 centidegree")

    def __str__(self):
        return str(self.Node_Temperature)

class MSG_Press_Attrubute(models.Model): # water pressure
    Node_Press = models.DecimalField(max_digits=6,decimal_places=2,default = 101.01,help_text = "water pressure, such as 101.01 KPa")
    def __str__(self):
        return str(self.Node_Press)

"""
原生节点(裸节点)，放置节点的时候，需要这三个信息：物理地址，地理位置以及逻辑序号
在实地使用的时候，一定会用逻辑序号来区分节点，而不会用MAC地址来区分节点，但对于这些原始节点来说，其内在的最大不同在于MAC地址，
"""
class Raw_Node(models.Model): #放置节点时，信息
    RawNode_ID = models.IntegerField(primary_key = True,help_text="节点逻辑序号,从1开始计数") #
    Geo_Address = models.CharField(max_length = 255, default = "", help_text = "node geography address")
    MAC_Address = models.CharField(max_length=18,default="",help_text="原始节点的物理地址") #可以认为在四五年内不会变更，因而是固定的
    
    def __str__(self):
        return str(self.RawNode_ID)

"""
时刻节点,以时间和原生节点为主键：表示某一时刻，节点的IP地址和收集到的信息
这里必须使用联合主键，因为IP地址，MSG既与时刻有关系，又与原生节点有关联
"""
from django.utils import timezone
class Time_Node(models.Model):
    Note_Time = models.DateTimeField(help_text="记录时间",auto_now_add=True)
    Note_Node = models.ForeignKey(Raw_Node,on_delete=models.SET_NULL,blank = True,null = True,help_text="原始节点")

    IP_Address = models.ForeignKey(Net_Attribute,on_delete = models.SET_NULL,null = True,blank = True,help_text="IP地址")

    Note_PH = models.ForeignKey(MSG_PH_Attribute,on_delete = models.SET_NULL,null = True,blank = True,help_text="PH value")
    Note_TP = models.ForeignKey(MSG_Temperature_Attribute,on_delete = models.SET_NULL,null = True,blank = True,help_text="temperature,(centidegree) ")
    Note_PS = models.ForeignKey(MSG_Press_Attrubute,on_delete = models.SET_NULL,null = True,blank = True,help_text="Pressure,(KPa)")

    class Meta:
        unique_together = ("Note_Time","Note_Node")
    
    def __str__(self):
        return str(self.Note_Time) + str(self.Note_Node)

    def get_absolute_url(self):
        return reverse("Time_Node_detail",args=[str(self.id)])

#仿真结果数据表
class Simultaion_Result(models.Model):
    Loss_Packet = models.DecimalField(max_digits=3,decimal_places=2,default = 0.00,help_text = "loss packet")
    Delay_Time = models.IntegerField(default=0,help_text="Millisecond")

    def __str__(self):
        return str(Loss_Packet)
#未完待续


"""
#硬件仿真数据表
本实验是一对一的实验，即一个发射节点，一个接收节点
"""

class Emulation_Test(models.Model):
    Test_Name = models.CharField(max_length = 100 , help_text = "test name") #测试用例名字
    Emul_Time = models.DateTimeField(help_text = "仿真时间" , auto_now=True)  #仿真开始时间

    #一次实验，选一个接收节点，一个发射节点。而每个节点都可能有多次实验
    Recv_Node = models.ForeignKey(Raw_Node, related_name="Recv",on_delete = models.SET_NULL,null = True,help_text="Recv Node") #
    Send_Node = models.ForeignKey(Raw_Node, related_name="Send",on_delete = models.SET_NULL,null = True,help_text="Send Node")

    Recv_File = models.FileField(help_text="Receive File",blank = True)
    Send_File = models.FileField(help_text="Send File",blank = True)

    def __str__(self):
        return ("%s,%s" % (self.Test_Name,str(Emul_Time)))

    def get_absolute_url(self):
        return reverse("Emulation_Test_detail",args=[str(self.id)])


"""=============================================================
留言板，数据库设计
================================================================"""

class Message_Board(models.Model):
    MSG_Time = models.DateTimeField(auto_now=True,help_text="留言时间")
    #留言者
    Commenter = models.ForeignKey(User,related_name="Commenter",on_delete=models.SET_NULL,null=True,blank=True,help_text="only registered user can user ite")
    LeavingMSG = models.CharField(max_length=250,help_text="leaving message")
    #评论者

"""
 =============================================================
class Topic(models.Model)
用户发起一个话题，
================================================================"""   
class Topic(models.Model):
    Title = models.CharField(max_length=30,help_text="the title of this topic") #话题主题
    #话题发起人
    Spoke_Man = models.ForeignKey(User,related_name="Spoke_Man",on_delete=models.SET_NULL,null=True,blank=True,help_text="only registered user can user ite")
    Content = models.TextField(max_length=250,help_text="talk about") #说了什么事情
    Spoke_Time = models.DateTimeField(auto_now=True,help_text="话题发起时间")
    #评论者
    Reviewer_MSG = models.ManyToManyField(Message_Board,default = None,help_text="留言")
    #点赞
    Good = models.IntegerField(default=0,help_text="点赞数量")
    def __str__(self):
        return self.Title
    
    def get_absolute_url(self):
        return reverse("comment_detail",args=[str(self.id)])


"""
pl
"""
class UanEmulation(models.Model): 
    # 1. taskID
    taskID = models.CharField(max_length=48, help_text = "the id of emulation task")
    
    # 2. user
    emuUser = models.ForeignKey(
        User, 
        related_name = "emuUser", 
        on_delete = models.SET_NULL, 
        null = True,
        blank = True, 
        help_text = "registered user can use"
    )
    
    # 3. the source file
    srcFilePath = models.CharField(max_length = 255, help_text = "the srcFilePath")
    
    # 4. the result of emulated files
    emuFilesPath = models.CharField(max_length = 255, help_text = "the emulated files ")
    
    # 5. emulated time
    emuTime = models.DateTimeField(auto_now = True, help_text = "the emulated time")
    
    # 6. src node
    srcNodeID = models.ForeignKey(
        Raw_Node, 
        related_name = "srcNodeId", 
        on_delete = models.DO_NOTHING,
        help_text = ""
    ) 

    def __str__(self):
        return self.taskID

    def get_absolute_url(self):
        return reverse("uanEmulatedDetail", args = [str(self.id)])

# 无人船信息
class Ship_msg(models.Model):
    Ship_ID = models.IntegerField(primary_key=True,default = 0, help_text="节点逻辑序号,从1开始计数")  #
    heading = models.FloatField(null=True, blank=True, help_text="偏航角0")
    pitch = models.FloatField(null=True, blank=True, help_text="俯仰角1")
    roll = models.FloatField(null=True, blank=True, help_text="横滚角2")
    poi_lat = models.FloatField(null=True, blank=True, help_text="维度3")
    poi_lng = models.FloatField(null=True, blank=True, help_text="经度4")
    alt = models.FloatField(null=True, blank=True, help_text="高度5")
    ve = models.FloatField(null=True, blank=True, help_text="东向速度6")
    vn = models.FloatField(null=True, blank=True, help_text="北向速度7")
    vu = models.FloatField(null=True, blank=True, help_text="天向速度8")
    other = models.CharField(max_length=255, default = '其他信息',help_text=" other")

    def __str__(self):
        return str(self.Ship_ID)

class onlineslist(models.Model):
    flag = models.IntegerField(primary_key=True,default = 0, help_text="无人船在线节点列表")
    nodelist = models.CharField(max_length=255,default= '',help_text="在线节点")


class shipp2ptest(models.Model):
    testname = models.CharField(max_length=255, help_text="testname")
    srcFilePath = models.CharField(max_length=255, help_text="the srcFilePath")
    recvFilesPath = models.CharField(max_length=255, help_text="the recv files ")
    testTime = models.DateTimeField(auto_now=True, help_text="the emulated time")

    def __str__(self):
        return self.srcFilePath

    def get_absolute_url(self):
        return reverse("shipp2p_detail", args=[str(self.id)])
    
