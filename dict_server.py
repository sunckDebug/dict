#!/usr/bin/env python3
#coding=utf-8

'''
name : zhang
date : 2018-09-28
email : 1741126544@qq.com
modules: python3.5  mysql  pymysql
This is a dict project for AID
'''

from socket import *
import os,pymysql,time,sys,signal

DICT = "./dict.txt"
HOST = ''
POST = 8000
ADDR = (HOST, POST)

def main():
    #创建数据库链接
    db = pymysql.connect\
    ('localhost','root','123456','dict')

    #创建流式套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    while True:
        try:
            c, addr = s.accept()
            print(addr,"已连接")
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器以退出")
        except Exception as err:
            print(err)
            continue


        #创建子进程
        p = os.fork()
        if p == 0:
            s.close()
            do_child(c, db)
            sys.exit(0)
        else:
            c.close()
            continue
    


def do_child(c, db):
    while True:
        data = c.recv(128).decode()
        print("Request:",data)
        if (not data) or data[0] == "E":
            c.close()
            sys.exit(0)
        if data[0] == "L":
            login(c, data, db)
        elif data[0] == "R":
            register(c, data, db)
        elif data[0] == "Q":
            query(c, data, db)
        elif data[0] == "H":
            history(c, data, db)



def login(c, data, db):
    l = data.split(" ")

    name = l[1]
    passwd = l[2]


    #查询用户表
    cursor = db.cursor()
    sql = \
    "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r == None:
        c.send(b'FALL')
    else:
        c.send(b'OK')




def register(c, data, db):
    l = data.split(" ")

    name = l[1]
    passwd = l[2]

    #查询用户表
    cursor = db.cursor()
    sql = \
    "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b'EXISTS')
        return

    sql = "insert into user(name,passwd)\
     values ('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FALL')
        return
    else:
        print("%s注册成功"%name)




def query(c, data, db):
    l = data.split(" ")

    word = l[1]
    name = l[2]

    #查询单词表
    cursor = db.cursor()
    sql = \
    "select * from words where word='%s'"%word
    cursor.execute(sql)
    r = cursor.fetchone()

    def insert_history():
        tm = time.ctime()
        sql = "insert into hist (name,word,time)\
         values ('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return


    if r == None:
        c.send(b'EXISTS')
        return
    insert_history()
    c.send(r[2].encode())


def history(c, data, db):
    l = data.split(" ")
    name = l[1]

    #查询历史记录表
    cursor = db.cursor()
    sql = \
    "select * from hist where name='%s'" % name
    cursor.execute(sql)
    r = cursor.fetchall()

    l = ""
    for i in r:
        for x in i:
            l = l + "#" + str(x)

    c.send(l.encode())
    return




if __name__ == "__main__":
    main()