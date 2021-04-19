from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns=[
    #path('',views.index,name="index"),
    url(r'^$',views.index,name="index"),
	#url(r'^home',views.index,name="index"),  #主页 
]
#当了没有登录的时候，进入的一个界面
urlpatterns+=[
    url(r'publichistory',views.publicHistory,name="publichistory"),
]
#管理人员界面
urlpatterns+=[
    path(r'management/',views.ManagementListView.as_view(),name="management_list"),#as_view()把类当作函数
    path(r'management/<int:pk>',views.ManagementDetailView.as_view(),name="management_detail"),  #详细界面
]

#
urlpatterns+=[
    path(r'simulationparament/',views.SimulationParamentListView.as_view(),name="simulationparament_list"),
    path(r'simulationparament/<int:pk>',views.SimulationParamentDetailView.as_view(),name="simulationparament_detail"),
]

#用户登录界面
urlpatterns+=[
    path(r'accounts/',include('django.contrib.auth.urls')),
]

#用户设置参数的位置
urlpatterns+=[
    path(r'simulationhistory/',views.simulationHistoryListView.as_view(),name="simulation_history"),
]

#在这里用户提交表单，运行仿真
urlpatterns+=[
    path(r'runningsimulation/',views.runningsimulation,name="runningsimulation"),
]

#删除一条仿真记录
urlpatterns+=[
    path(r'simulationhistory/<int:pk>',views.delete_store_info,name="delete"),
]

#实现下载功能
urlpatterns+=[
    path(r'simulationhistory/<int:pf>/download',views.downloadfile,name='download'),
]

#终端测
urlpatterns+=[   
    path(r'terminalssh/<int:nodeId>',views.terminalSSH,name="terminalSSH"),
    path(r'terminalSelector', views.selectNodeTerminal, name = "terminalSelector")
]

#节点环境参赛表
urlpatterns+=[
    path(r'nodeEnviro',views.nodeEnviro,name="nodeEnviro")
]
#硬件仿真
urlpatterns+=[
    path(r'hardware_emulation',views.hardwareEmulation,name="hardwareEmulation")
]

urlpatterns+=[
    path(r'ns3_simulation',views.uanEmulationForNs3,name="ns3Simulation")
]
#讨论区，
urlpatterns+=[
    path(r'comment',views.commentArea,name="comment")
]
#我的讨论区
urlpatterns+=[
    path(r'my_comment',views.getMyComment,name="my_comment")
]
#删除我的一条讨论
urlpatterns+=[
    path(r'my_comment/<int:pf>',views.deleteMyComment,name="delete_mycomment")
]
#点赞一条评论
urlpatterns+=[
    path(r'comment/<int:pf>',views.goodComment,name="GoodComment")
]
#test1
# 查看在线节点
urlpatterns+=[
    path(r'viewOnlineNodes', views.viewOnlineNodes, name = "viewOnline"),
    path(r'viewOneNode/<int:nodeId>', views.viewOneNode, name = "viewOneNode"),
    path(r'viewUanEmulation', views.uanEmulation, name = "viewUanEmulation"),
    path(r'uanHistory', views.UanEmulationListView.as_view(), name = "uanHistory"),
    path(r'uanHistory/<int:pf>/delete', views.deleteUanEmulation, name = "uan_delete"),
    path(r'uanHistory/<int:pf>/downloadSource', views.downloadUanEmulationSource, name = "uanSourceDownload"),
    path(r'uanHistory/<int:pf>/downloadResult', views.downloadUanEmulationResult, name = 'uanResultDownload')
]

# ship
urlpatterns+=[
    # path(r'viewpoision', views.viewpoision, name = "viewpoision"),
    path(r'poirefresh', views.poirefresh, name = "datarefresh"),
    path(r'viewonlinenodemsg/msgrefresh', views.msgarefresh, name = "msgdatarefresh"),
    path(r'viewonlinenodemsg/sendcommand', views.sendcommand, name = "sendcommand"),
    path(r'viewonlinenodemsg/sendarea', views.sendarea, name = "sendarea"),
    path(r'viewonlinenodemsg/sendpointroute', views.sendpointroute, name = "sendpointroute"),
    path(r'viewonlinenodemsg/sendlineroute', views.sendlineroute, name = "sendlineroute"),
    path(r'viewonlinenodemsg/<int:nodeId>', views.onlinenodemsg, name = "onlinenodemsg"),
]

#nodetest
urlpatterns+=[
    path(r'nodetest', views.nodetest, name = "nodetest"),
    path(r'shiphistory', views.shiplistview.as_view(), name="shiphistory"),
    path(r'shipHistory/<int:pf>/downloadSource', views.downloadshipEmulationSource, name = "shipSourceDownload"),
    path(r'shipHistory/<int:pf>/downloadResult', views.downloadshipEmulationResult, name = "shipResultDownload"),
    path(r'shipHistory/<int:pf>/delete', views.deleteshipEmulation, name = "ship_delete"),


]