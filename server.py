"""
一。功能
 1，向所有已连接的用户发送用户列表信息
 2，接收用户连接请求，以及下线指示。
 3，退出程序

 二，框架的设计
 1，向所有已连接的用户发送用户列表信息 send_msg()
 2,接收用户连接请求，以及下线指示。 recv_msg()
 3,程序的主入口 main
 4，程序对立运行的时候，才启动聊天器
 三，实行步骤
 1，发送信息send_msg()
 1) ，遍历用户信息表单
 2），使用socket的sendto（） 向每个用户发送用户表单信息

 2，接收信息 recv_msg()
 1)使用socket接收数据
 2）解码数据
 3）判断用户是上线还是下线
 3.1） 增加用户表单 client_append()
  1)在表单末尾增加上线用户的ip和端口号
 3.2） 减少用户表单client_remove()
  1)根据下线用户的ip和端口号，删除下线用户信息
 4)调用send_msg()

 3主入口
 1）创建套接字
 2）绑定端口
 3）循环监听以及发送
 4）关闭套接字
"""

import socket
import json

client_list = []

def send_msg(udp_socket):
    """向所有已连接的用户发送用户列表信息"""
    # 1)，遍历用户信息表单
    for x in client_list:
        # 2），使用socket的sendto（） 向每个用户发送用户表单信息
        cotent = json.dumps(client_list)
        udp_socket.sendto(cotent.encode(), x)


def recv_msg(udp_socket):
    """接收用户连接请求，以及下线指示。"""
    while True:
        # 1)使用socket接收数据
        recv_data, ip_port = udp_socket.recvfrom(1024)
        # 2）解码数据
        recv_text = recv_data.decode()
        # 3）输出显示
        if recv_text == '请求上线':
            client_list.append(ip_port)
            print(ip_port,"已上线")
            print(client_list,len(client_list))
            send_msg(udp_socket)
        elif recv_text == '请求下线':
            client_list.remove(ip_port)
            print(ip_port, "已下线")
            print(client_list, len(client_list))
            send_msg(udp_socket)
        else:
            continue


def main():
    """程序的主入口"""
    # 1）创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2）绑定端口
    # address --> (“IP地址”，8080)
    # udp_sockeet.bind(adress)
    print(client_list,len(client_list))
    udp_socket.bind(("", 8080))
    # 循环监听以及发送
    recv_msg(udp_socket)
    # 4）关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    # 程序独立运行的时候才被调用
    main()