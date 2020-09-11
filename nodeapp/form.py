from django import forms
from django.forms import fields
#class param(forms.Form):
#读取用户提交的参数
class SubmitRunningMessage(forms.Form):
    #调制方式
    Modulation = fields.ChoiceField(
        choices=(('QPSK','QPSK'),('MFSK','MFSK'),),
        required=True,
        label="调制方式",
    )
    #MAC协议
    MACPtorocols =fields.ChoiceField(
        choices=(('simple-aloha','simple-aloha'),('pure-aloha','pure-aloha'),),
        required=True,
        label="MAC协议",
    )
    #路由协议
    Route = fields.ChoiceField(
        choices=(('Static-routing','Static-routing'),('Dynamic-routing','Dynamic-routing'),),
        required=True,
        label="路由协议",
    )
    #传输层协议
    Transport = fields.ChoiceField(
        choices=(('TCP','TCP'),('UDP','UDP'),),
        required=True,
        label="传输层协议",
    )
    #应用层协议
    Application = fields.ChoiceField(
        choices=(('CBR','CBR'),('VBR','VBR'),),
        required=True,
        label="应用层协议",
    )
    #仿真方式
    Simulation = fields.ChoiceField(
        choices=(('simulation','simulation'),('emulation','emulation'),),
        required=True,
        label="仿真方式",
    )
    #实验名称
    TestName = forms.CharField(
        error_messages={'required':"实验名称不能为空"},
        label="实验名称",
    )  

class OnlineNodes(forms.Form):
    NumNodes=forms.IntegerField(
        label="Number of nodes",
        initial=0 #初始值为0
    )
#硬件仿真时，处理上传文件
class Emulation_Test_File_Form(forms.Form):
    #Test_Name = forms.CharField(label="实验名称",max_length=100)
    UpLoad_File = forms.Field(label="文件上传")

#开启一个话题
class Topic_Form(forms.Form):
    Title =  fields.ChoiceField(
        choices=(("Emulation","硬件仿真"),("Simulation","软件仿真"),("Web","网站建设"),("Others","其他问题")),
        required=True,
        label="话题"
    )
    Content = forms.CharField(widget = forms.Textarea,max_length=250,help_text="talk about") #说了什么事情
