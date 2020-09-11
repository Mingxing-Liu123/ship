# 导入模块
import socket
import threading


# 接收消息
def recv(client_socket, ip_port):
    while True:
        client_text = client_socket.recv(1024)
        # 如果接收的消息长度不为0，则将其解码输出
        if client_text:
            print("[客户端消息]", ip_port, ":", client_text.decode("utf-8"))
            # 给客户端响应
            client_socket.send("收到\n".encode('utf-8'))
        # 当客户端断开连接时，会一直发送''空字符串，所以长度为0已下线
        else:
            print("客户端", ip_port, "已下线")
            client_socket.close()
            break


# 程序主入口
def main():
    # 创建TCP套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口复用
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口
    tcp_socket.bind(("", 8080))
    # 设置为被动监听状态，128表示最大连接数
    tcp_socket.listen(128)
    while True:
        # 等待客户端连接
        client_socket, ip_port = tcp_socket.accept()
        print("[新客户端]:", ip_port, "已连接")
        # 有客户端连接后，创建一个线程将客户端套接字，IP端口传入recv函数，
        t1 = threading.Thread(target=recv, args=(client_socket, ip_port))
        # 设置线程守护
        t1.setDaemon(True)
        # 启动线程
        t1.start()


if __name__ == '__main__':
    main()