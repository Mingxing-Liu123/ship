#!/usr/bin/python3

#============================================================
#本文件主要存放两个类，HandlerSSHConnection(threading.Thread)和
#class SSHConsumer(WebsocketConsumer)。类SSHConsumer主要处理
#websocket连接，HandlerSSHConnection主要处理网站后台与ssh的远程连接。
#============================================================

# ==================================================
# 第二版处理SSH请求的函数
# HandlerSSHConnection，通过用epoll来监控ssh连接的channels，
# 通过轮询来监控共享的全局变量django_to_ssh，因为涉及线程之间的同步
# 。因此，采用锁机制，这是使用互斥锁
# =====================================================
from asgiref.sync import async_to_sync #异步转同步
import paramiko, threading, select
from .handlerFile import ConfigCenter

django_to_ssh = ""
mutex_lock = threading.Lock()

class DjangoToSshProxy:
    _instance = None
    #_flag = False
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def setCommunicateData(self, communicateData = ""):
        global mutex_lock
        global django_to_ssh
        
        mutex_lock.acquire() # lock
        django_to_ssh = communicateData
        mutex_lock.release() # release the lockv

    def getCommunicateData(self):
        global mutex_lock
        global django_to_ssh
    
        resData = ""
        mutex_lock.acquire()
        resData = django_to_ssh
        mutex_lock.release()
        return resData

class HandlerSSHConnection(threading.Thread):
    def __init__(self,SshConsumer):
        threading.Thread.__init__(self)
        self.SshConsumer = SshConsumer #

    def run(self):
        try:
            self.handleSshIOData()
        except Exception as e:
            print("exception:", e)
        finally:            
            self.SshConsumer.Channel.close()
            dToSshProxy = DjangoToSshProxy()
            dToSshProxy.setCommunicateData("")

    def handleSshIOData(self):
        global django_to_ssh #
        Epoll = select.epoll()
        Epoll.register(self.SshConsumer.Channel, select.EPOLLIN)
        while True:  #自己轮询
            events = Epoll.poll(0.001)
            for fileno, event in events:
                if fileno == self.SshConsumer.Channel.fileno(): 
                    result_str = self.SshConsumer.Channel.recv(1024).decode()
                    #print("\r\n result_str: "+result_str +"\r\n")
                    async_to_sync(self.SshConsumer.channel_layer.group_send)( #
                        self.SshConsumer.scope['user'].username,{
                            "type":"user.message",
                            "text":result_str
                        },
                    )
            dToSshProxy = DjangoToSshProxy()
            communicateData = dToSshProxy.getCommunicateData()
            if len(communicateData) != 0: #全局变量不为空
                self.SshConsumer.Channel.sendall(communicateData)
                print("input to ssh:", communicateData)
                dToSshProxy.setCommunicateData("")


# SSHConsumer(WebsocketConsumer),继承了WebsocketConsumer，因而可以使用
# websocketconsumer的函数send来给前端的websocket客户端发送消息
from channels.generic.websocket import WebsocketConsumer
class SSHConsumer(WebsocketConsumer):
    def connect(self): #相当于初始化，只不过以调用这个类或者对象，首先执行这个函数
        print("------connect------")
        #创建channels_group，命名为:用户名,并使用channel_layer写入到redis
        async_to_sync(self.channel_layer.group_add)(
            self.scope['user'].username,
            self.channel_name
        )
        self.accept()
        self.buildSshConnection()

    def disconnect(self,close_code):
        print("disconnect,")
        async_to_sync(self.channel_layer.group_discard)(
            self.scope['user'].username,
            self.channel_name
        )
        self.Channel.close()

    def receive(self,text_data):
        #print("receive date: "+ text_data)
        dToSshProxy = DjangoToSshProxy()
        dToSshProxy.setCommunicateData(text_data)

    def user_message(self,event):
        #print("user_message:" + event['text'])
        self.send(text_data=event['text']) #发给前端

    def buildSshConnection(self):
        print("========connect", self.scope['url_route']['kwargs'])
        nodeIDstr = self.scope['url_route']['kwargs']['nodeID']
        try:
            config = ConfigCenter()
            nodeAccount = config.getNodeAccount(int(nodeIDstr))
            print("accoutn:", nodeAccount)
            Trans = paramiko.Transport(nodeAccount["ipv4"],22)
            Trans.start_client()
            Trans.auth_password(username=nodeAccount["userName"],password=nodeAccount["passWord"])

            self.Channel = Trans.open_session()
            self.Channel.get_pty()
            self.Channel.invoke_shell()

            t1 = HandlerSSHConnection(self)
            t1.setDaemon = True
            t1.start()
        except Exception as e:
            print(e)
            self.send("can't link with server")

