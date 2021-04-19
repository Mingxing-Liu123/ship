# -*-coding:utf-8-*-
# from  .ship_recQue import shiprecvQue
# import threading
# from .ship_result import ship_results
# from ..handlerDB import saveshipdata
#
# class ship_RecvManager(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         while True:
#             shiprecvQue.delrest()
#             length = shiprecvQue.getQueLen()
#             if length < 3:
#                 continue
#             datalen = getdatalen()
#             # print("处理线程data_length:",datalen,shiprecvQue.m_que)
#             while True:
#                 if shiprecvQue.getQueLen() < datalen:
#                     continue
#                 contentlist = shiprecvQue.getNBytes(datalen)
#                 if len(contentlist) <= 0:
#                     break
#                 if len(contentlist) < 6:
#                     ship_results.otherdata = contentlist
#                     print("other1:",ship_results.otherdata)
#                     break
#                 if contentlist[0] == '$' and contentlist[5] == 'D':
#                     parse_gphpd(contentlist)
#                     break
#                 else:
#                     ship_results.otherdata = contentlist
#                     print("other2:",ship_results.otherdata)
#                     break
#
#
# def parse_gphpd(contentlist):
#     contentlist = contentlist[7:]
#     arg = {}
#     i = 0
#     preindex = 0
#     for index in range(len(contentlist)):
#         if contentlist[index] == ',':
#             arg[i] = contentlist[preindex:index]
#             preindex = index + 1
#             i = i + 1
#     arg[i] = str(contentlist[preindex:])
#     processdata = [None]*20
#     for index in range(len(arg) - 1):
#         lt = arg[index]
#         processdata[index] = float(''.join(lt))
#     saveshipdata(processdata)
#     print("recvadmin:",processdata)
#
# def getdatalen():
#     datalen = 0
#     lengthlist = shiprecvQue.getNBytes(2)
#     if lengthlist[1] == ',':
#         datalen = int(lengthlist[0])
#         return datalen
#     else :
#         lengthlist += shiprecvQue.getNBytes(1)
#         if lengthlist[2] == ',':
#             datalen = int(lengthlist[0]) * 10 + int(lengthlist[1])
#             return datalen
#         else:
#             datalen = int(lengthlist[0])*100 +int(lengthlist[1])*10 +int(lengthlist[2])
#             shiprecvQue.getNBytes(1)
#             return datalen
