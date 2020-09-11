# -*-coding:utf-8-*-
from math import cos, sin, atan2, sqrt, radians, degrees
def creatcenter(geolist = []):
    arg = []
    x = 0
    y = 0
    z = 0
    lng0 = None
    lat0 = None
    lng1 = None
    lat1 = None
    lon = None
    lat = None
    lng0 = radians(float(geolist[0]))
    lat0 = radians(float(geolist[1]))
    lng1 = radians(float(geolist[2]))
    lat1 = radians(float(geolist[3]))
    x = (cos(lat0) * sin(lng0) + cos(lat1) * sin(lng1)) / 2
    y = (cos(lat0) * cos(lng0) + cos(lat1) * cos(lng1)) / 2
    z = (sin(lat0) + sin(lat1)) / 2
    lng = degrees(atan2(x, y))
    lat = degrees(atan2(z, sqrt(x * x + y * y)))
    arg.append(str(lng)[0:11])
    arg.append(str(lat)[0:10])
    return arg

def creatpnode(p,geolist = []):
    arg = []
    x = 0
    y = 0
    z = 0
    lng0 = None
    lat0 = None
    lng1 = None
    lat1 = None
    lon = None
    lat = None
    # print(geolist,geolist[0],type(geolist[0]))
    lng0 = radians(float(geolist[0]))
    lat0 = radians(float(geolist[1]))
    lng1 = radians(float(geolist[2]))
    lat1 = radians(float(geolist[3]))
    for index in range(p):
        x = cos(lat0) * sin(lng0) + (cos(lat1) * sin(lng1) -cos(lat0) * sin(lng0))/ (p+1) * (index +1)
        y = cos(lat0) * cos(lng0) + (cos(lat1) * cos(lng1)-cos(lat0) * cos(lng0))/(p+1) * (index +1)
        z = sin(lat0) + (sin(lat1) - sin(lat0))/ (p+1) * (index +1)
        lng = degrees(atan2(x, y))
        lat = degrees(atan2(z, sqrt(x * x + y * y)))
        arg.append(str(lng)[0:11])
        arg.append(str(lat)[0:10])
    return arg