# dict_client.py
from socket import *
import sys,re
import getpass
from prettytable import PrettyTable  # 美化库，PrettyTable模块可以将输出内容如表格方式整齐地输出

#创建网络链接
def main():
    if len(sys.argv) < 3:
        print("输入格式有误：请按以下 xxxxx   127.0.0.1 8000")

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    s = socket()
    s.connect(ADDR)

    while True:
        print('''\n
            ===========Welcome=========
            --1.注册    2.登录    3.退出--
            ===========================
            ''')
        try:
            cmd = input("请输入命令")
        except Exception as err:
            print("命令错误")
            continue

        if cmd in ["1","2","3"]:
            if cmd == "1":
                name = register(s)
                print(name)
                if name != False:
                    print("注册成功")
                    do_login(s,name)
                elif name == False:
                    print("用户已存在")
                else:
                    print("注册失败")
            elif cmd == "2":
                name = login(s)
                print(name)
                if name != False:
                    print("登录成功")
                    do_login(s,name)
                elif name == False:
                    print("登录不成功")
            elif cmd == "3":
                s.send(b"E")
                sys.exit("感谢使用")
        else:
            print("没有你输入的命令")
            sys.stdin.flush() #清除输入
            continue


def login(s):
    user = input("请输入用户名:")
    passwd = getpass.getpass("请输入密码:")


    print("用户名%s 密码%s" % (user,passwd))
    msg = "L {} {}".format(user,passwd)

    s.send(msg.encode())

    data = s.recv(128).decode()
    if data == "OK":
        return user
    else:
        return False

def register(s):
    while True:
        
        name = input("请输入用户名:")
        if not name:
            print("<<@用户名不能为空@>>")
            continue
        passwd = getpass.getpass("请输入密码:")
        if not passwd:
            print("<<#密码不能为空#>>")
            continue
        qpasswd = getpass.getpass("确认密码:")
        if not qpasswd:
            print("<<*确认密码不能为空*>>")
            continue
        if qpasswd != passwd:
            print("<<$两次密码不一致$>>")
            continue
        if (' ' in name) or (' ' in passwd):
            print("<<??用户名密码不允许有空格!!>>")
            continue


        print("用户名%s 密码%s" % (name,passwd))
        msg = "R {} {}".format(name,passwd)

        s.send(msg.encode())

        data = s.recv(128).decode()
        if data == "OK":
            return name
        elif data == "EXISTS":
            return False
        else:
            return False


def do_login(s, name):
    while True:
        print('''\n
            ================查询界面=================
            |<$1.查词$>    <$2.历史记录$>   <$3.注销$>|
            ========================================
            ''')
        
        try:
            cmd = int(input("<<$请输入命令$>>"))
        except Exception:
            print("命令错误")
            continue

        if cmd in [1,2,3]:
            if cmd == 1:
                query(s, name)
            elif cmd == 2:
                history(s)
            elif cmd == 3:
                return
        else:
            print("没有您输入的命令")
            sys.stdin.flush() #清除输入



def query(s, name):
    while True:
        word = input("请输入要查询的单词")
        if word == "##":
            return
        msg = "Q {} {}".format(word,name)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == "OK":
            data = s.recv(1024).decode()
            print(data)
        else:
            print(data)




def history(s):
    name = input("输入要查询历史的用户：")
    msg = "H {}".format(name)
    print(name)
    s.send(msg.encode())
    data = s.recv(2048).decode()
    data = data.split("#")


    n = 0
    x = PrettyTable(["<<$ID$>>","<<$name$>>","<<$word$>>","<<$date$>>"])
    while True:
        x.add_row([data[1+n],data[2+n],data[3+n],data[4+n]])
        n += 4
        if n >= len(data)-4:
            break

    print(x)




if __name__ == "__main__":
    main()