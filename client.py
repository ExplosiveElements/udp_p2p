"""
一。功能
 1，发送功能
 2，接收功能
 3，退出程序

 二，框架的设计
 1，发送信息 send_msg()
 2,接收的信息 recv_msg()
 3,程序的主入口 main
 4，程序对立运行的时候，才启动聊天器
 三，实行步骤
 1，发送信息send_msg()
 0）展示用户列表
 1)，定义变量接收用户与输入的接收方的IP地址
 2），定义变量接收用户与输入的接收方的端口
 3），定义变量接收用户与输入的接收方的内容
 4），使用socket的sendto（） 发送信息

 2，接收信息 recv_msg()
 1)使用socket接收数据
 2）通过ip和端口号判断是由服务器还是由其他客户端发送的消息
 3）解码数据
 4.1）接收服务器发来的用户表单以更新
  1）client_list = new_clieent_list
  2)显示新的用户表单
 4.2) 显示其他客户端的信息
 3主入口
 1）创建套接字
 2）绑定端口
 3）打印菜单（循环）
 4）接收用户的输入选项
 5）判断用户的选择，并调用对应的函数
 6）关闭套接字
"""

import socket
import threading
import json

client_list = []
server = ("192.168.88.1",8080) # 服务器的地址

def send_msg(udp_socket):
    """发送信息的函数"""
    # 0）展示用户列表
    print("现在的用户表单：",client_list)
    # 1)，定义变量接收用户与输入的接收方的IP地址
    ipaddr = input("请输入接收方的ip地址：\n")
    # 2），定义变量接收用户与输入的接收方的端口
    port = input("请输入要发送的端口号：\n")
    # 3），定义变量接收用户与输入的接收方的内容
    cotent = input("请输入要发送的信息:\n")
    # 4），使用socket的sendto（） 发送信息
    udp_socket.sendto(cotent.encode(), (ipaddr, int(port)))


def recv_msg(udp_socket):
    """接收信息的函数"""
    while True:
        # 1)使用socket接收数据
        recv_data, ip_port = udp_socket.recvfrom(1024)
        # 通过ip和端口号判断是由服务器还是由其他客户端发送的消息
        if ip_port == server:
            # 3）解码数据
            new_clieent_list = json.loads(recv_data)
            # 4.1)接收服务器发来的用户表单以更新
            global client_list
            client_list = new_clieent_list
            print("现在的用户表单",client_list)
        else:
            # 3）解码数据
            recv_text = recv_data.decode()
            # 4.2)显示其他客户端的信息
            print("从【%s】收到的消息：%s" % (str(ip_port), recv_text))


def main():
    """程序的主入口"""
    # 1）创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2）绑定端口
    # address --> (“IP地址”，8081)
    # udp_sockeet.bind(adress)
    udp_socket.bind(("", 8081))
    # 获取本机ip
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    # 发送上线请求
    udp_socket.sendto('请求上线'.encode(), server)
    # 创建子线程单独接收用户发送的信息
    thread_recv = threading.Thread(target=recv_msg,args=(udp_socket, ))
    # 守护进程
    thread_recv.setDaemon(True)
    # 启动子线程
    thread_recv.start()
    while True:
        # 3）打印菜单（循环）
        print("本机ip【%s】和端口号【8081】" % myaddr)
        print("1,发送信息")
        print("2,关闭程序")
        # 4）接收用户的输入选项
        sel_num = int(input("请输入选项：\n"))
        # 5）判断用户的选择，并调用对应的函数
        if sel_num == 1:
            # 调用发送信息的函数
            send_msg(udp_socket)
        elif sel_num == 2:
            # 发送下线请求
            udp_socket.sendto('请求下线'.encode(), server)
            print("系统正在退出。。。")
            print("系统退出完成！")
            break
    # 6）关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    # 程序独立运行的时候才被调用
    main()