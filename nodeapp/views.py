#!/usr/bin/python3
#视图文件，放置所有视图函数
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
#---------------------------------------------------------
# def publicHistory(request) :  显示首页的函数
# ---------------------------------------------------------
def publicHistory(request):
    return render(
        request,
        "Simulation/publichistory.html",
        context={},
    )

from django.views import generic
from . import models


class ManagementListView(generic.ListView):
    model = models.Management
    template_name = "Manager/management_list.html"
class ManagementDetailView(generic.DetailView):
    model = models.Management
    template_name = "Manager/management_detail.html"

class SimulationParamentDetailView(generic.DetailView):
    model = models.SimulationParament
    template_name = "Simulation/simulationparament_detail.html"

class SimulationParamentListView(generic.ListView):
    model = models.SimulationParament
    template_name = "Simulation/simulationparament_list.html"
#
class RawNodeListView(generic.ListView):
    model = models.Raw_Node
class RawNodeDetailView(generic.DetailView):
    model = models.Raw_Node
#
class TimeNodeListView(generic.ListView):
    model = models.Time_Node
class TimeNodeDetailView(generic.DetailView):
    model = models.Time_Node

#用户参数设置视图,用于查看过往仿真历史,只有登录用户可以调用
from django.contrib.auth.mixins import LoginRequiredMixin
class simulationHistoryListView(LoginRequiredMixin,generic.ListView):
    model = models.SimulationParament #调用数据模型为SimulationParament，该模型存放了仿真参数
    template_name="Simulation/simulation_history.html"
    paginate_by=10 #设置最多显示10个，多的就另起一页

    def get_queryset(self):
        return models.SimulationParament.objects.filter(SimulationUser=self.request.user)

from .form import SubmitRunningMessage  #通过表单模块读取仿真参数
import json  #调用json相关函数以执行js文件
from .tasks import client_update
from . import handlerDB


def runningsimulation(request): 
    MACLIST=["00:00:00:00:00:01","00:00:00:00:00:02","00:00:00:00:00:03"] #这个列表用来测试用的------------------------------
    online_nodes=0  #初始化在线节点为0
    OUTPUT ={"Loss":"---","Delay": "---","Throughput":"---"}  #初始化仿真结果
    #POST请求
    if request.method == 'POST':
        form_request = SubmitRunningMessage(request.POST)  #读取设置的参数，读取form表单（方式：POST）
        
        if "agree_submit" in request.POST:
            if form_request.is_valid():#检查字符
               #先把
                RecvMAC = request.POST['recvnode']  #这两个没有使用表单模块，接收机电MAC
                SendMAC = request.POST['sendnode']  #

                Modulation = form_request.cleaned_data['Modulation']
                MACPtorocols = form_request.cleaned_data['MACPtorocols']
                Route = form_request.cleaned_data['Route']
    
                Transport = form_request.cleaned_data['Transport']
                Application = form_request.cleaned_data['Application']
                Simulation = form_request.cleaned_data['Simulation']
                TestName = form_request.cleaned_data['TestName']
                #添加到数据库中  
                inputparamentlist = [ #10个元素
                    RecvMAC,SendMAC,Modulation,MACPtorocols,
                    Route,Transport,Application,Simulation,
                    request.user,TestName
                ] 
                handleSimulationParament = handlerDB.HandleSimulationParament()    
                handleSimulationParament.saveSimulationParaments(inputparamentlist)

                inputparamentlist.pop() #删除用户名，实验名
                inputparamentlist.pop()
                #inputparamentlist.append(dataid)

                client_update.delay(inputparamentlist)  ############ 运行仿真
                print(inputparamentlist)

                feedback=["运行成功","run successfully"]
                return render(
                    request,
                    'Simulation/runningsimulation.html',
                    {
                        'form_request':form_request,
                        'feedback':json.dumps(feedback),
                        'online_nodes':online_nodes,
                        'OUTPUT':OUTPUT,
                        'MACLIST':MACLIST
                    }
                )
        else:   #当点击刷新按钮的时候，
            form_request=SubmitRunningMessage() #这个函数在这里的作用在于不用管参数是否设置，直接运行相关函数用来查看有多少个节点
            #这里将用celery来实现异步通
            MACLIST = client_update.delay([]) #传送一个空列表，使得连接ns3的socket函数知道是请求返回在线节点数量
            #online_nodes = len(MACLIST)

            print("shuaxing------")
            return render(
                request,
                "Simulation/runningsimulation.html",
                {
                    'form_request':form_request,
                    'OUTPUT':OUTPUT,
                    'MACLIST':MACLIST.get(timeout=20),
                }
            )
            
    #当是GET的时候,或者说正常访问的时候,即打开或者刷新网页的时候
    else:
        form_request=SubmitRunningMessage()
        online_nodes = 1

    return render(
        request,
        'Simulation/runningsimulation.html',
        {
            'form_request':form_request,
            #'List':json.dumps(LIST),
            'online_nodes':online_nodes,
            'OUTPUT':OUTPUT,
            'MACLIST':MACLIST,
        }
    )  
    
# --------------------------------------------------------------
# def delete_store_info(request,pk)
# 删除一条主键为pk的仿真信息
# --------------------------------------------------------------
from .handlerDB import deleteSimulationParament
def delete_store_info(request,pk):
    print("primarykey = " + str(pk))
    Result = deleteSimulationParament(pk)
    
    if Result == False:
        print("Failed to delete data : " )
        return HttpResponse('Failed to delete data')
    else:
        return HttpResponseRedirect('/nodeapp/simulationhistory/')


# -------------------------------------------------------------
# def downloadfile(request,pf)
# 实现下载功能，就目前来说，下载的是文本文档，
# 接下来会考虑下载CSV文档或者Excel文档
# -------------------------------------------------------------
from django.http import StreamingHttpResponse
from . import handlerFile

def downloadfile(request,pf):
    if not request.user.is_authenticated:
        return HttpResponse("please login in")

    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    #写入文件
    the_file_name ="history.txt"
    result = handlerFile.writeSimulationToFile(the_file_name,pf)
    if result == False:
        return HttpResponse("Error")

    response =StreamingHttpResponse(file_iterator(the_file_name))   #这里创建返回
    response['Content-Type'] = 'application/octet-stream'   #注意格式 
    response['Content-Disposition'] = 'attachment;filename="history.txt"'   #注意filename 这个是下载后的名字
    return response


# ---------------------------------------------------------
# def terminalSSH(request): #为终端测试界面视图
# ---------------------------------------------------------
from .handlerFile import ConfigCenter

# 选择连接哪个终端
def selectNodeTerminal(request):
    if not request.user.is_authenticated:
        return render(
            request,
            "index.html"
        )
    config = ConfigCenter() # read config
    nodeIDs = config.getNodes()
    return render(
        request,
        "WebTerminal/terminal.html",
        {
            "nodeId":0
        }
    )
#---------------------------------------------------------
#def nodeEnviro(request): 
#水声节点的环境
#---------------------------------------------------------"""
def nodeEnviro(request):
    return render(
        request,
        "Emulation/envir_param.html",
    )
#硬件仿真
from .tasks import Get_Oline_Nodes
#from .handlerFile import saveUploadedFile
from .handlerDB import getRawNodes
def hardwareEmulation(request):
    if not request.user.is_authenticated: # 用户不合法
        print("invalid")
        return render(
            request,
            "Emulation/hardware_emulation.html"
        )
    #用户合法的条件下
    All_Nodes = [] #所有节点
    #Operate_Result = ""
    UpLoadFile_Result = ""
    if request.method == "POST": 
        if "SeeNode" in request.POST: #查看多少节点
            SeeNode_result = request.POST.get("See")
            print(SeeNode_result)
            if SeeNode_result == "All Nodes": #查看数据库的节点
                All_Nodes = getRawNodes() # 把调用异步任务（这里没有使用异步），获取mac_list列表
            elif SeeNode_result == "Online Nodes": #查看在线节点
                All_Nodes = Get_Oline_Nodes()

        else : # 开始仿真
            TestName = request.POST.get("Test_Name")
            UpLoadFile = request.FILES.get("SendFile")
            if not UpLoadFile:
                print("上传失败")
                return HttpResponse("上传失败") 
            else: #这里必须要把这个上传文件写入到磁盘上，因为NS-3仿真平台需要这样一个文件来进行数据通信，如果不在磁盘上写入一个文件，那么这个文件将存在与内存之中，
                #当跳出该函数的时候，这个临时内存将释放
                print(UpLoadFile.name)
                #write_status = saveUploadedFile(UpLoadFile)
                if write_status == False:
                    UpLoadFile_Result = "由于系统有待完善，上传文件格式必须为UTF-8格式，望谅解"
                #上传并成功写入到磁盘文件后
    return render(
        request,
        "Emulation/hardware_emulation.html",
        {
            "All_Nodes":All_Nodes, #
            'UpLoadFile_Result':ns3_simulation,
        }
    )



"""
===========================================================
def commentArea(request)
留言板
==========================================================="""

from .models import Topic
from .form import Topic_Form
def commentArea(request):
    #对所有人都可见
    TopicForm = Topic_Form()
    Access_Right = False
    #if not request.auth.is_authenticated: #没有登陆
    All_Topics = Topic.objects.all()

    if request.method == "POST" and request.user.is_authenticated:
        Access_Right =True
        Post_Form = Topic_Form(request.POST)
        if Post_Form.is_valid():
            print(Post_Form.cleaned_data["Title"])
            
            new_topic = Topic()
            new_topic.Title = Post_Form.cleaned_data["Title"]
            new_topic.Spoke_Man = request.user
            new_topic.Content = Post_Form.cleaned_data["Content"]
            new_topic.save()
            
    return render(
        request,
        "Comment/comment.html",
        {
            "All_Topics1":All_Topics,
            "TopicForm":TopicForm,
            "Access":Access_Right,
        }
    )
"""
===================================================================
我的评论
==================================================================="""
def getMyComment(request):
    if not request.user.is_authenticated:
        return render(
            request,
            "nodeapp/index.html"
        )
    My_Topics = Topic.objects.filter(Spoke_Man = request.user)

    return render(
        request,
        "Comment/my_comment.html",
        {
            "My_Topics":My_Topics,
        }
    )
"""
===================================================================
删除我的评论
===================================================================
"""
def deleteMyComment(request,pf):
    if not request.user.is_authenticated:
        return HttpResponse("sorry,you have no access to delete this date!")
    try:
        getMyComment = Topic.objects.get(id = pf)
    except e:
        print(e)
        return HttpResponse("Can't find you date")
    else:
        getMyComment.delete()
    
    return HttpResponseRedirect("/nodeapp/my_comment")

"""
===================================================================
给某条评论点赞
顶一下，踩一下
===================================================================
"""

def goodComment(request,pf):
    #游客也可以使用
    try:
        The_Comment = Topic.objects.get(id = pf)
    except e:
        print(e)
        return HttpResponse("Sorry, The Comment has been deleted")
    else:
        The_Comment.Good = The_Comment.Good +1 
        The_Comment.save()

    return HttpResponseRedirect("/nodeapp/comment")

#"""
#===================================================================
#查看在线节点数量,以及查看节点情况
#===================================================================
#"""
from .uan import uan_client
from .uanEmulation import UanNodeAdmin
def viewOnlineNodes(request):
    # print("viewOnlineNodes")
    nodeIdList = []
    isLogin = False
    nodeAdmin = UanNodeAdmin()
    if request.method == "GET":
        if request.user.is_authenticated:  
            nodeIdList = nodeAdmin.getOnlineNodes()
            isLogin = True 
    elif request.method == "POST":  #
        if request.user.is_authenticated:
            nodeIdList = nodeAdmin.getOnlineNodes()
            isLogin = True 
            viewNodes = request.POST.getlist("nodeID")        
            viewNodeList = []
            for nodeIdStr in viewNodes:
                viewNodeList.append(int(nodeIdStr))

            client = uan_client.UanSimulationClient()
            
            nodesMsg = client.getNodeMsg(viewNodeList)

    return render(
        request,
        "Emulation/RealTimeMonitor.html",
        {
            "nodeIDs":nodeIdList
        }
    )

"""
=================================================================
look at one nodes
=================================================================
"""
def viewOneNode(request, nodeId):
    geoAddress = "west lake"
    tp = 16.4
    press = 101
    ph = 6.7
    if request.user.is_authenticated:
        ip = "lab"
    
    return render(
        request,
        "Emulation/Node_detail.html",
        {
            "nodeID":nodeId,
            "geoAddr":geoAddress,
            "temperature":tp,
            "ph":ph,
            "pressure":press
        }
    )
from .handlerDB import UanEmulationDBHandler
# this function receive UAN simulation data
def uanEmulation(request):
    onlineNodes = []
    emulatedStatus = "None"
    if request.user.is_authenticated:
        if request.method == "GET":
            nodeAdmin = UanNodeAdmin()
            onlineNodes = nodeAdmin.getOnlineNodes()

        elif request.method == "POST" : # post
            userFile = request.FILES.get("emuFile")
            sendNodeId = request.POST.get("sendNodeId")
            recvNodeIds = request.POST.getlist("recvNodeIds") 
             
            if userFile:
                client = uan_client.UanSimulationClient()
                taskId = client.getTaskId()
                # print("taskId, ",taskId)
                
                nodeIds = []
                nodeIds.append(int(sendNodeId))
                for nodeId in recvNodeIds:
                    nodeIds.append(int(nodeId))
                
                fileSaver = handlerFile.saveUANEmulationResultToFile(
                        userFile,
                        taskId,
                        nodeIds)
                filePath = fileSaver.save()
                # print("filePath:",filePath)
                UanEmulationDBHandler.saveParamBeforeEmulated(
                    taskId, 
                    request.user,
                    filePath, 
                    nodeIds[0], 
                    nodeIds[1:]
                )

                #client.getFileResult(nodeIds, filePath)
                client.async_getFileResult(
                    nodeIds, 
                    filePath, 
                    taskId, 
                    UanEmulationDBHandler.saveResultAfterEmulated # callback
                )

                emulatedStatus = "Running"
    return render(
        request,
        "Emulation/uan_emulation.html",
        {
            "onlineNodes": onlineNodes,
            "emulatedStatus":emulatedStatus
        }
    )

def terminalSSH(request, nodeId):
    if not request.user.is_authenticated:
        return render(
            request,
            "index.html",
        )
    nodeIdInt = nodeId
    onlineNodes = []
    emulatedStatus = "None"
    if request.user.is_authenticated:
        if request.method == "GET":
            nodeAdmin = UanNodeAdmin()
            onlineNodes = nodeAdmin.getOnlineNodes()

        elif request.method == "POST":  # post
            userFile = request.FILES.get("emuFile")
            sendNodeId = request.POST.get("sendNodeId")
            recvNodeIds = request.POST.getlist("recvNodeIds")

            if userFile:
                client = uan_client.UanSimulationClient()
                taskId = client.getTaskId()
                # print("taskId, ",taskId)

                nodeIds = []
                nodeIds.append(int(sendNodeId))
                for nodeId in recvNodeIds:
                    nodeIds.append(int(nodeId))

                fileSaver = handlerFile.saveUANEmulationResultToFile(
                    userFile,
                    taskId,
                    nodeIds)
                filePath = fileSaver.save()
                # print("filePath:",filePath)
                UanEmulationDBHandler.saveParamBeforeEmulated(
                    taskId,
                    request.user,
                    filePath,
                    nodeIds[0],
                    nodeIds[1:]
                )

                # client.getFileResult(nodeIds, filePath)
                client.async_getFileResult(
                    nodeIds,
                    filePath,
                    taskId,
                    UanEmulationDBHandler.saveResultAfterEmulated  # callback
                )
    return render(
        request,
        "WebTerminal/terminal.html",
        {
            "nodeId":nodeIdInt,
            "onlineNodes": onlineNodes
        }
    )

def uanEmulationForNs3(request):

    if request.user.is_authenticated:
        if request.method == "POST" : # post
            return HttpResponse("ok");
        else:
            return render(
                    request,
                    "Emulation/uan_ns3_simulation.html"
                    )
    else:
        return HttpResponseRedirect("/nodeapp/accounts/login")
class UanEmulationListView(generic.ListView):
    model = models.UanEmulation
    template_name = "Emulation/uan_history.html"

def downloadUanEmulationSource(request, pf):
    if not request.user.is_authenticated:
        return HttpResponse("please login in")

    taskId = handlerDB.UanEmulationDBHandler.getEmuTaskId(pf)
    print("get taskID:", taskId)
    if len(taskId) == 0:
        return HttpResponse("can't find the result, please input correct one")

    zipHandler = handlerFile.UanResultZip(taskId)
    if not zipHandler.hasendzipfile():
        zipHandler.createZipFile(2)
    sendzipFilePath = zipHandler.getsendZipFileDir()

    def file_iterator(file_name, chunk_size=512):  # 用于形成二进制数据
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # 写入文件

    response = StreamingHttpResponse(file_iterator(sendzipFilePath))  # 这里创建返回
    response['Content-Type'] = 'application/octet-stream'  # 注意格式
    response['Content-Disposition'] = 'attachment;filename=source"'  # 注意filename 这个是下载后的名字
    response['Content-Disposition'] +=  '.zip"'
    return response
    # if not request.user.is_authenticated:
    #     return HttpResponse("please login in")
    #
    # def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
    #     with open(file_name,'rb') as f:
    #         while True:
    #             c = f.read(chunk_size)
    #             if c:
    #                 yield c
    #             else:
    #                 break
    # #写入文件
    # filePath = handlerDB.UanEmulationDBHandler.getSrcFilePath(primaryKey = pf)
    # if len(filePath) == 0:
    #     return HttpResponse("error emulation")
    #
    # fileNameList = filePath.split('/')
    # fileName = fileNameList[-1]
    #
    # response =StreamingHttpResponse(file_iterator(filePath))   #这里创建返回
    # response['Content-Type'] = 'application/octet-stream'   #注意格式
    # response['Content-Disposition'] = 'attachment;filename="'   #注意filename 这个是下载后的名字
    # response['Content-Disposition'] += fileName + '"'
    # return response

def deleteUanEmulation(request, pf): 
    if not request.user.is_authenticated:
        return HttpResponse("please login in")
    
    handlerDB.UanEmulationDBHandler.deleteParam(primaryKey = pf)
    return HttpResponseRedirect("/nodeapp/uanHistory")


def downloadUanEmulationResult(request, pf):
    if not request.user.is_authenticated:
        return HttpResponse("please login in")
    
    taskId = handlerDB.UanEmulationDBHandler.getEmuTaskId(pf)
    print("get taskID:", taskId)
    if len(taskId) == 0:
        return HttpResponse("can't find the result, please input correct one")

    zipHandler = handlerFile.UanResultZip(taskId)
    if not zipHandler.hasZipFile():
        zipHandler.createZipFile(1)
    zipFilePath = zipHandler.getZipFileDir()

    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    #写入文件

    response =StreamingHttpResponse(file_iterator(zipFilePath))   #这里创建返回
    response['Content-Type'] = 'application/octet-stream'   #注意格式 
    response['Content-Disposition'] = 'attachment;filename=recv"'   #注意filename 这个是下载后的名字
    response['Content-Disposition'] += '.zip"'
    return response        

# ---------------------------------------------------------
# def index(request):  显示首页的函数
# ---------------------------------------------------------
from .ship import route, Socket_tcp
def index(request):
    tcp_ser=Socket_tcp.tcp_serlisen()
    onlinens = []
    return render(
        request,
        "index1.html",
        {
            "onlinenodes": onlinens,
        }
    )

####发送命令到无人船进行远程控制
def sendcommand(request):
    if request.method == 'POST':
        nodeid = request.POST.get('nodeid')
        # print("comment前端发来的：",nodeid,type(nodeid))
        tcp_ser = Socket_tcp.tcp_serlisen()
        res=tcp_ser.sendtocli('hello', nodeid)
        # res = ship_send.sendcomtoship()
        if res == True:
            return HttpResponse("OK!")
    return HttpResponse("error")
###发送点到无人船
def sendpointroute(request):
    tcp_listen = Socket_tcp.tcp_serlisen()
    if request.method == 'POST':
        print("line前端发来的：aaa")
        nodeid = request.POST.get('nodeid')
        if 'lineroute' in request.POST:
            poilist = []
            poilist = request.POST.getlist('lineroute', [])
            print("初始发送的点:", poilist, len(poilist) / 2)
            linelen = int(len(poilist) / 2 - 1)  # 线段数目
            addnode = int(10 - (len(poilist) / 2))  # 要加点的个数
            if len(poilist) <= 20:  # 无人船接收端只能接受10个点,若不够,则加点
                if linelen >= addnode:  # 线段数目大于等于要加点的个数
                    for index in range(addnode):
                        center = route.creatcenter(poilist[4 * index:4 * index + 4])
                        poilist.insert(4 * index + 2, center[0])
                        poilist.insert(4 * index + 3, center[1])
                        # print(center)
                    # print(poilist,len(poilist))
                else:
                    z = int(addnode // linelen)
                    y = int(addnode % linelen)
                    # print(z,y)
                    for index in range(linelen):
                        newnode = route.creatpnode(z, poilist[(2 + 2 * z) * index:(2 + 2 * z) * index + 4])
                        # print("增加的点1:",newnode)
                        for i in range(len(newnode)):
                            poilist.insert((2 + 2 * z) * index + 2 + i, newnode[i])
                        # print(poilist)
                    if y != 0:
                        newnode = route.creatpnode(y, poilist[0:4])
                        # print("增加的点2:", newnode)
                        for index in range(len(newnode)):
                            poilist.insert(2 + index, newnode[index])
                print("补充发送的点:", poilist, len(poilist) / 2)
                # res = ship_send.sendlinetoship(poilist,nodeid)
                res = False
                for index in range(int(len(poilist) / 2)):
                    msg = '$,'
                    msg += poilist[index * 2]
                    msg += ','
                    msg += poilist[index * 2 + 1]
                    sendmsg = msg + ',*'
                    # tcp_send = Socket_tcp.tcp_serlisen()
                    res = tcp_listen.sendtocli(sendmsg, nodeid)
                if res == True:
                    return HttpResponse("OK!")
            else:
                return HttpResponse("error")
    return HttpResponse("error")
######发送线段到无人船
def sendlineroute(request):
    tcp_listen = Socket_tcp.tcp_serlisen()
    if request.method == 'POST':
        nodeid = request.POST.get('nodeid')
        # print("line前端发来的：",nodeid)
        if 'lineroute' in request.POST:
            poilist = []
            poilist = request.POST.getlist('lineroute',[])
            print("初始发送的点:",poilist,len(poilist)/2)
            linelen =int(len(poilist)/2 -1) #线段数目
            addnode = int(10 -(len(poilist)/2)) #要加点的个数
            if len(poilist) <= 20:     #无人船接收端只能接受10个点,若不够,则加点
                if linelen >= addnode: #线段数目大于等于要加点的个数
                    for index in range(addnode):
                        center = route.creatcenter(poilist[4*index:4*index+4])
                        poilist.insert(4*index+2,center[0])
                        poilist.insert(4*index+3,center[1])
                        # print(center)
                    # print(poilist,len(poilist))
                else:
                    z = int(addnode // linelen)
                    y = int(addnode % linelen)
                    # print(z,y)
                    for index in range(linelen):
                        newnode =route.creatpnode(z,poilist[(2 +2*z)*index:(2 +2*z)*index+4])
                        # print("增加的点1:",newnode)
                        for i in range(len(newnode)):
                            poilist.insert((2+2*z)*index+2+i,newnode[i])
                        # print(poilist)
                    if y != 0:
                        newnode = route.creatpnode(y, poilist[0:4])
                        # print("增加的点2:", newnode)
                        for index in range(len(newnode)):
                            poilist.insert(2+index,newnode[index])
                print("补充发送的点:",poilist,len(poilist)/2)
                # res = ship_send.sendlinetoship(poilist,nodeid)
                res = False
                for index in range(int(len(poilist) / 2)):
                    msg = '$,'
                    msg += poilist[index * 2]
                    msg += ','
                    msg += poilist[index * 2 + 1]
                    sendmsg = msg + ',*'
                    # tcp_send = Socket_tcp.tcp_serlisen()
                    res = tcp_listen.sendtocli(sendmsg, nodeid)
                if res == True:
                    return HttpResponse("OK!")
            else:
                return HttpResponse("error")
    return HttpResponse("error")

########发送区域到无人船
def sendarea(request):
    if request.method == 'POST':
        if 'route' in request.POST:
            poilist = request.POST.getlist('route',[])
            print(len(poilist))
            return HttpResponse("OK!")
        return HttpResponse("error")


from .handlerFile import get_from_file_nodes
def poirefresh(request):
    # tcp_listen = tcp_serlisen()
    if request.method == 'POST':
        onlinenodes = get_from_file_nodes()
        # onlinenodes=[1,2]
        sort_onlinenodes = sorted(onlinenodes)
        # print("在线节点：",onlinenodes)
        poilist = handlerDB.getshippoision(sort_onlinenodes)
        ajax_map ={'onlinenodes':sort_onlinenodes,'poilist':poilist}
        # print("ajax_map:",ajax_map)
        return HttpResponse(json.dumps(ajax_map))
    return HttpResponse("error")

def msgarefresh(request):
    if request.method == 'POST':
        if 'nodeid' in request.POST:
            node_id = request.POST.get('nodeid')
            # print("nodeid:",node_id)
        msglist = handlerDB.getshipmsg(node_id).copy()
        return HttpResponse(json.dumps(msglist))
    return HttpResponse("error")


def onlinenodemsg(request, nodeId):
    if not request.user.is_authenticated:
        return render(
            request,
            "index.html",
        )
    nodeid = nodeId
    # print("xxxxxxx:",nodeid)
    # msglist = handlerDB.getshipmsg(nodeid).copy()
    return render(
        request,
        "ship/nodemsg1.html",
        {
            "nodeId": nodeid
            # "msglist": msglist
        }
    )

from .form import shipp2p_Form
from .handlerDB import saveship_p2p_para
import threading

def nodetest(request):
    tcp_listen = Socket_tcp.tcp_serlisen()
    onlinens=[]
    res = False
    if request.user.is_authenticated:
        if request.method == "GET":
            onlinens = get_from_file_nodes()
            form_request = shipp2p_Form()
        elif request.method == "POST":
            form_request = shipp2p_Form(request.POST)
            if form_request.is_valid():  # 检查字符
                TestName = form_request.cleaned_data['TestName']
                # print("testname:",TestName)
                userFile = request.FILES.get("emuFile")
                sendNodeId = request.POST.get("sendNodeId")
                recvNodeIds = request.POST.getlist("recvNodeIds")
                print("sendnode,recvnodes",sendNodeId,recvNodeIds,recvNodeIds[0])

                if userFile:
                    #FTP服务器文件路径
                    file_dir = "/home/vsftp/ftp/"
                    # file_dir = "/home/lmx/lmx/"
                    fire_name = file_dir + userFile.name
                    # print(fire_name)
                    with open(fire_name, 'wb') as fp:
                        for chunk in userFile.chunks():
                            try:
                                fp.write(chunk)
                            except Exception as e:
                                print("saveUploadFile exception,", e)
                    # 数据格式:001,fileneme,recvnodeid
                    res = tcp_listen.sendtocli('001,'+userFile.name+','+str(recvNodeIds[0]),int(sendNodeId))
                    if res == True:
                        saveship_p2p_para(TestName,userFile.name)
                        t1 = threading.Thread(target=checkrecvfile, args=(userFile.name, TestName))
                        t1.start()
    return render(
        request,
        "ship/node_communicate.html",
        {
            "sendstate": res,
            "nodeId": onlinens,
            "form_request":form_request
        }
    )

import os
import time
def checkrecvfile(filename,testname):
    # file_dir = "/home/lmx/lmx/"
    file_dir = "/home/vsftp/ftp/"
    filepath = file_dir+'r'+filename
    for i in range (30):
        if(os.path.exists(filepath)):
            handlerDB.saverecvfileresult(testname,filename)
            print("接收文件已到达")
            break
        time.sleep(2)

class shiplistview(generic.ListView):
    model = models.shipp2ptest
    template_name = "ship/ship_history.html"

def downloadshipEmulationSource(request, pf):
    if not request.user.is_authenticated:
            return HttpResponse("please login in")

    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        #写入文件
    filePath = handlerDB.getshipsourcedir(primaryKey = pf)
    # filePath = "/home/lmx/lmx/"+ filePath
    filePath = "/home/vsftp/ftp/"+ filePath
    if len(filePath) == 0:
        return HttpResponse("error emulation")

    response =StreamingHttpResponse(file_iterator(filePath))   #这里创建返回
    response['Content-Type'] = 'application/octet-stream'   #注意格式
    response['Content-Disposition'] = 'attachment;filename=source'   #注意filename 这个是下载后的名字
    response['Content-Disposition'] +=   '.DA'
    return response

def downloadshipEmulationResult(request, pf):
    if not request.user.is_authenticated:
            return HttpResponse("please login in")

    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        #写入文件
    filePath = handlerDB.getshipResultdir(primaryKey = pf)
    # filePath = "/home/lmx/lmx/" + filePath
    filePath = "/home/vsftp/ftp/" + filePath
    if len(filePath) == 0:
        return HttpResponse("error emulation")

    response =StreamingHttpResponse(file_iterator(filePath))   #这里创建返回
    response['Content-Type'] = 'application/octet-stream'   #注意格式
    response['Content-Disposition'] = 'attachment;filename=recv'   #注意filename 这个是下载后的名字
    response['Content-Disposition'] +=   '.DA'
    return response

def deleteshipEmulation(request, pf):
    if not request.user.is_authenticated:
        return HttpResponse("please login in")
    handlerDB.deleteshipParam(primaryKey=pf)
    return HttpResponseRedirect("/nodeapp/shiphistory")