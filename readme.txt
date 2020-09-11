超级用户：water
密码：lab408408

普通用户：xiaoming
密码：lab00000

安装环境：
django 2.0.7
celery 4.
channel 
paramiko

# 1. webssh和网页终端心得
## 1.1 django 使用思路
使用channels模块，

```bash
channels
包含两个部分
1. consumer.py 相当于view.py
2. routing.py 相当于url.py

一个channel 层，提供两个抽象
1. 一个channel是一个消息可以发送到达的邮箱，
2. 一个群组是一群有关联的channel
```

## 1.2 paramiko使用SSH思路
参考网站
<a href="https://www.jianshu.com/p/8d1766c23523">简书：paramiko</a>

```py
#基于用户名和密码的transport方式登陆

import paramiko
#实例化一个连接
trans = paramiko.Transport("127.0.0.1",22)
"""
如果基于公钥密钥的连接，则需要设置密码
pkey = paramiko.RSAKey.from_private_key_file("/home/xiaokang/.ssh/id_rsa",password="123456")
"""
#建立连接
trans.connect(username="xiaokang",password="123456")

#实例化一个SSH远程连接SSHClient连接
ssh = paramiko.SSHClient()
ssh._transport = trans

#执行命令
stdin,stdout,stderr = ssh.exec_command("ls -l")
print(stdout.read().decode())
trans.close()
```

# 2. 数据库设计思路
## 2.1 软件仿真版 
## 2.2 硬件仿真版
```txt
其实对节点进行数据存储很简单，只要把所有信息都写到一张数据表里就行。
本人在此不屑于这种粗暴简单的做法，特此考虑关系型数据库的三大范式，而作第二版数据库——硬件仿真数据库

一个节点主要有以下几个信息：  
    1. 节点物理地址（MAC address）
    2. 节点逻辑序号（逻辑ID）
    3. 节点地理位置
    4. 节点网络地址（IPv4 address）
    5. 节点采集信息数据（MSG）
        5.1 PH值
        5.2 温度（temperature）
        5.3 压强（pressure）
        ……
    
其次考虑到节点处于网络当中，因此IPv4地址是可变的，而节点处于水里，因此采集到的数据MSG也是变化的，最后如果更换设备，也可能导致物理地址变化，
```
由于MAC地址，IPv4地址，地理地址，MSG_ph，MSG_pressure,MSG_temperature是相互独立的，不互相依赖。根据三大范式，数据表的列不可细分，数据表不存在联合主键，数据表不存在传递以来主键，因而对于这些属性，均独自构造一张数据表

因为在海洋，湖泊中放置节点的时候肯定会对每个节点进行标号，这个标号是固定的，是从1开始的，节点坏了还可以另外放置一个，但这个序号是固定的。
**因此，以逻辑序号为主键构建节点表**
对于节点表，考虑到只有在某一时刻谈论其IPv4地址，MSG才有意义，否则抛开时刻讨论这些，无异于耍流氓。

Raw_Node表
|逻辑序号（NumberID）（主键）| MAC Address | 地理位置（可写可不写） | 
|---|---|---|

Time_Node表
| 时刻（主键） |Raw_Node(主键)|  网络地址（IPv4） | MSG |
|---|---|---|---|
IP地址和MSG依赖与时刻和Raw_Node, 即这两个属性依赖联合主键
在同一时刻，可以有多个Raw_Node,

对于时刻节点表，每个节点都可以在多个时刻对应有多个IP地址，MSG信息
# 3. 文件上传
文件上传，在前端的表单有一个重要设置
```html
<form action="{% url 'hardwareEmulation' %}" method="POST" name="start_emulation" enctype="multipart/form-data">
<input type = "file" name="send_file">
<input type = "submit" value= "提交">
</form>
```
其中，这个enctype="multipart/form-data"必不可少，少了前端就不能上传文件到后台，

而后台部门，
```py
RecvFile = request.FILES.get("send_file")
#这个RecvFile是<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>类型的
#如果接收失败，返回null

```

# 4 与NS-3仿真平台的接口设计标准
## 4.1 通信标准
&emsp;&emsp;与NS-3仿真平台通信的情况有以下两种：

1. 软件仿真
2. 硬件仿真

## 4.2 socket方案
### 4.2.1 软件通信标准
socket方案，将django传送给NS-3仿真平台的数据列表，转成字符串。NS-3仿真平台也将返回字符串

* **1. 查看节点数量，并要求放回**

django 传送字符串给NS-3仿真平台：**“ModemRequest”**

如果查阅成功：
NS-3仿真平台返回“Sucess;MAC1;MAC2;……”,其中S：success
，如果失败，则返回字符串“Failed”:failed

伪代码如下所示
```py
#查看节点
simulation_result = django_to_NS3("ModemRequest")
result_list = simulation_result.split(";")
if len(result_list) == 1:
    print("查看失败")
else:
    print("查看成功")
```

* **2. 执行软件仿真**
django 传送字符给NS-3仿真平台;“SimulationStart;”+[ #10个元素
                    RecvMAC,SendMAC,Modulation,MACPtorocols,
                    Route,Transport,Application,Simulation,
                    request.user,TestName
                ]  

如果仿真成功，则返回 “Ok;TimeDelay=123;PacketLoss=123;AverageThroughput=123;PrimaryKey=123”

如果仿真失败，则返回“Failed”

### 4.2.2 硬件仿真通信标准
* **1. 查看某个节点状态**
django 发送 **“ANodeStatus;MACID”**

在NS-3仿真平台看来，这些仿真节点总共有三种状态：能联系上并处于休闲状态，能联系上但处于忙碌状态，失联状态

如果NS-3仿真平台返回的信息如下所示：
1. “Failed;Dispear”: 表示失联状态
2. “Failed;Busy”:表示节点正忙碌，不能执行接下来的仿真任务
3. "Failed;MACError":表示MAC地址错误
3. “Success;”:表示节点可以进行接下来的仿真工作，

* **2.查看节点在线数量**
和软件仿真一样,django 发送 **“ModemRequest”**

* **3. 获取节点信息**
```bash
首先django 得确定该节点是否处于可以进行仿真工作，

django 首先发送  "ANodeStatus;MACID" 

如果NS-3返回 "Failed" ,那么返回获取失败
如果NS-3返回 "Success"，那么
django 发送 "ANodeMSG"

NS-3受到后，返回 "ph;temperature;press;IPv4"
```

* **4. 执行仿真**
这里涉及到进程之间共享文件，因此有待思考
