# -*-coding:utf-8-*-
def main():
	# msg = '$GPHPD,1688,357049.190,66.61,-0.34,10.26,'
	msg2 = '113.352997,56.122,-4920.200,56712.901,-288.918,0.004,0.024,-0.001,0.020,0.011,-0.019,1.808,15,15,4*60'
	# msg +='x'
	# print(msg)
	lat = 23.162138
	for index in range(10):
		msg = '$GPHPD,1688,357049.190,66.61,-0.34,10.26,'
		lat = lat + 0.00005
		print(lat,type(lat))
		msg +=(str(lat))[0:9]
		msg +=','
		for i in range(len(msg2)):
			msg += msg2[i]
		print(msg)
	# z = int(y1)
	# print(x,x.to_bytes(length=2,byteorder="big"),)
	# print("ascii",y.encode('ascii'))
	# print("utf-8",y.encode('utf-8'))
	# print("utf-8", y1.encode('ascii'))
	# print(type(y1),int(y1))
	# print("z:",float(z)*2)

if __name__ == '__main__':
	main()


