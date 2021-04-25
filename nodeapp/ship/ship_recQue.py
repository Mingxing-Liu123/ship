# -*-coding:utf-8-*-
import threading

class shipRecvQue:
    __instance = None
    lock = threading.RLock()

    def __init__(self):
        if not self.__instance:
            print('调用__init__， shipRecvQue未创建')
            self.fdmap = {}
            self.onlinenodes=[]
            self.content=[]
        else:
            print('调用__init__，shipRecvQue已经创建过了')

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.lock.acquire()
            if not cls.__instance:
                cls.__instance = shipRecvQue()
            cls.lock.release()
        return cls.__instance