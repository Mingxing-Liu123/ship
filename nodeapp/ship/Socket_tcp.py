# -*-coding:utf-8-*-from nodeapp.ship.ship_recvTread import serthreadfrom nodeapp.ship.ship_recQue import shipRecvQueimport threadingclass tcp_serlisen:    __instance = None    _initFlag = False    lock = threading.RLock()    def __new__(cls):        if cls.__instance is None:            # print("tcp new1")            cls.lock.acquire()            if cls.__instance is None:                # print("tcp new2")                cls.__instance = super().__new__(cls)            cls.lock.release()        return cls.__instance    def __init__(self, port=6378):        if not self._initFlag:            self._initFlag=True            print('调用__init__， tcp_serlisen未创建')            self.m_port = port            self.m_fd = -1            self.start()        else:            print('调用__init__，tcp_serlisen已经创建过了')    def start(self):        r = serthread(self.m_port)        r.start()    def sendtocli(self,msg = '',cli = None):        try:            self.m_fd = shipRecvQue.get_instance().fdmap[int(cli)]            self.m_fd.send(msg.encode())            return True        except Exception as e:            return False