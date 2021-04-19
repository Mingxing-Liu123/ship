# -*-coding:utf-8-*-
import threading

class Ship_Result:
    _instance = None
    _initFlag = False
    lock = threading.RLock()

    def __new__(cls):
        if cls._instance is None:
            cls.lock.acquire()
            if cls._instance is None:
                # print("construct UAN_Result")
                cls._instance = super().__new__(cls)
            cls.lock.release()
        return cls._instance

    def __init__(self):
        if self._initFlag == False:
            self._initFlag = True
            self.otherdata = []
            # self.results = [None]*20
            self.gphpd_data = [1694.0, 357049.190, 62.61, -0.34, 10.26, 39.9607816, 116.2858456, 56.122, -4920.200,56712.901, -288.918, 0.004, 0.024, -0.001, 0.020, 0.011, -0.019, 1.808, 15.0, 15.0]
            # 设初始值
            # '$GPHPD,1694,357049.190,62.61,-0.34,10.26,39.9607816,116.2858456,56.122,-4920.200,56712.901,-288.918,0.004,0.024,
            # -0.001,0.020,0.011,-0.019,1.808,15,15,4*60'
            #msg1存放GPHPD协议的上述数据
            # self.gpsweek = 0.0 #星期数0
            # self.gpstime = 0.0 #熊期内秒数1
            # self.heading = 0.0 #偏航角2
            # self.pitch = 0.0 #俯仰角3
            # self.roll = 0.0 #横滚角4
            # self.lat = 0.0 #维度5
            # self.lon = 0.0 #经度6
            # self.alt = 0.0 #高度7
            # self.de = 0.0 #移动站相对于基站的东向距离8
            # self.dn = 0.0 #........北向距离9
            # self.du = 0.0 #........天向距离10
            # self.ve = 0.0 #东向速度11
            # self.vn = 0.0 #北向速度12
            # self.vu = 0.0 #天向速度13
            # self.ae = 0.0 #两次测量值之间的东向速度差14
            # self.an = 0.0 #.........北向速度差15
            # self.au = 0.0 #.........天向速度差16
            # self.bl = 0.0 #基线长度17
            # self.nsv1 = 0 #前天线可用星数18
            # self.nsv2 = 0 #后.........19

    def parse_GPHPD(self, datamap ={}):
        if len(datamap) <= 0:
            return False
        arg = [None]*20
        for index in range(len(datamap) - 1):
            lt = datamap[index]
            # self.gphpd_data.append(float(''.join(lt)))
            arg[index] = float(''.join(lt))

        return arg

        # return True

