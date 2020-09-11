# -*-coding:utf-8-*-
"""tcp服务器"""
import socket


def main():
	# 创建一个服务器socket
	socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 设置立即重置端口号
	socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# 绑定端口
	socket_server.bind(('',8002))
	# 设置被动连接 128 代表3次握手4次挥手建立链接的可链接客户端数
	socket_server.listen(128)
	while True:
		print("开始监听")
		client_socket, client_address = socket_server.accept()
		# 与客户端通信
		client_socket.send(b't')
		while True:
			recv_data = client_socket.recv(4096)
			if not recv_data:
				break
			print(recv_data,type(recv_data))
			print(recv_data[0],type(recv_data[0]))
			print(recv_data[0:2],type(recv_data[0:2]))
			recvdata = recv_data[0:2].decode()
			print(recvdata[0],type(recvdata[0]))
			print(int(recvdata[0])*3,type(int(recvdata[0])*3))
		client_socket.shutdown(2)
		client_socket.close()
		# 通信完关闭
		# 关闭 上面是死循环  伪关闭
	socket_server.close()


if __name__ == '__main__':
	main()
