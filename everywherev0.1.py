#! /usr/bin/env python
# coding: utf8
# version:v0.1
# code by: xiong.mingjun
"""
Change log:
v0.1 主要用于跟everywhere系统对接，功能有用户注册和积分查询
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from Tkinter import *
from tkMessageBox import *
import httplib
import base64
import json

class MyFrame():
    """Test for MyFrame"""

    hosturl = "everywhereshop.mybluemix.net"
    auth_key = 'Basic ' + base64.b64encode('xxxxx:xxxxx')
    dic_header = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': auth_key
    }

    # 定义主窗口和两个框架
    master = Tk()
    frame1 = Frame(master)
    frame2 = Frame(master)

    # 定义控件的值
    vfirst_name = StringVar()
    vlast_name = StringVar()
    vuid = StringVar()
    vphone = StringVar()
    vemail = StringVar()

    # 初始化字段的值
    str_first_name = ''
    str_last_name = ''
    str_uid = ''
    str_phone_number = ''
    str_email = ''

    # 定义菜单选项对应的变量
    vChoose = StringVar()

    # 定义窗口的所有控件，label为提示语，text为输入控件
    # 其中空行也使用了label
    label1 = Label(frame1, text='姓：')
    text1 = Entry(frame1, textvariable=vfirst_name)
    label2 = Label(frame1, text='名：')
    text2 = Entry(frame1, textvariable=vlast_name)
    label3 = Label(frame1, text='电话：')
    text3 = Entry(frame1, textvariable=vphone)
    label4 = Label(frame1, text='IMEI：')
    text4 = Entry(frame1, textvariable=vuid)
    label5 = Label(frame1, text='Email：')
    text5 = Entry(frame1, textvariable=vemail)
    button1 = Button(frame1, text='提交')
    button2 = Button(frame1, text='清空')
    text6 = Text(frame2)
    label6 = Label(frame1, text='')                  # 输入框和按钮之间的空行
    label7 = Label(frame1, text='用户注册', fg='blue')
    label8 = Label(frame1, text='积分查询', fg='blue')
    label9 = Label(frame1, text='*', fg='red')             # 必填项后面的*号，一共五个，目前最多的一个api里面有五个必填项
    label10 = Label(frame1, text='*', fg='red')
    label11 = Label(frame1, text='*', fg='red')
    label12 = Label(frame1, text='*', fg='red')
    label13 = Label(frame1, text='*', fg='red')
    label14 = Label(frame1, text='')                  # frame1里面，按钮下面的空行

    # 定义构造函数
    def __init__(self):
        # 新建菜单
        menubar = Menu(self.master)
        # 定义菜单选项栏
        tradetype = Menu(menubar)
        # 添加单选按钮到菜单选项
        tradetype.add_radiobutton(label='用户注册', command=self.regCustomer, variable=self.vChoose)
        tradetype.add_radiobutton(label='积分查询', command=self.queryPoint, variable=self.vChoose)
        menubar.add_cascade(label='选择交易类型', menu=tradetype)
        self.frame1.pack(fill=BOTH)
        self.frame2.pack(fill=BOTH)
        # 设置主窗口标题
        self.master.wm_title('everywhere接口v0.1')
        # 设置窗口大小
        self.master.geometry('300x400')
        # 限制改变窗口大小
        self.master.resizable(width=False, height=False)
        # 显示菜单条
        self.master.config(menu=menubar)

    def regCustomer(self):
        self.forgetAll()
        self.label7.grid(row=0)
        self.label1.grid(row=1, sticky=E)
        self.text1.grid(row=1, column=1)
        self.label9.grid(row=1, column=2)
        self.label2.grid(row=2, sticky=E)
        self.text2.grid(row=2, column=1)
        self.label10.grid(row=2, column=2)
        self.label3.grid(row=3, sticky=E)
        self.text3.grid(row=3, column=1)
        self.label11.grid(row=3, column=2)
        self.label4.grid(row=4, sticky=E)
        self.text4.grid(row=4, column=1)
        self.label12.grid(row=4, column=2)
        self.label5.grid(row=5, sticky=E)
        self.text5.grid(row=5, column=1)
        self.label13.grid(row=5, column=2)
        self.label6.grid(row=6)
        self.button1 = Button(self.frame1, text='提交', width=6, command=self.submit)
        self.button2 = Button(self.frame1, text='清空', width=6, command=self.clearAll)
        self.button1.grid(row=7)
        self.button2.grid(row=7, column=1)
        self.label14.grid(row=8)
        
    def queryPoint(self):
        self.forgetAll()
        self.label8.grid(row=0)
        self.label4.grid(row=1, sticky=E)
        self.text4.grid(row=1, column=1)
        self.label9.grid(row=1, column=2)
        self.label6.grid(row=2)
        self.button1 = Button(self.frame1, text='提交', width=6, command=self.submit)
        self.button2 = Button(self.frame1, text='清空', width=6, command=self.clearAll)
        self.button1.grid(row=3)
        self.button2.grid(row=3, column=1)
        self.label14.grid(row=4)

    def submit(self):
        self.text6.pack_forget()
        # 用于请求用户注册
        if '用户注册' == self.vChoose.get():
            if '' != self.vfirst_name.get() and '' != self.vlast_name.get() and '' != self.vuid.get() and '' != self.vphone.get() and '' != self.vemail.get():
                dict_msg = {'first_name': self.vfirst_name.get(), 'last_name': self.vlast_name.get(), 'uid': self.vuid.get(), 'phone': self.vphone.get(), 'email': self.vemail.get()}
                conn_http = httplib.HTTPConnection(self.hosturl)
                conn_http.request('POST', '/user', json.dumps(dict_msg), self.dic_header)
                res = conn_http.getresponse()
                if res.status == 200 or res.status == 201:
                    # 请求成功，背景为绿色；失败则为红色
                    self.text6 = Text(self.frame2, bg='green')
                    self.text6.pack(fill=BOTH)
                    self.text6.insert(INSERT, self.vChoose.get()+'\n')
                    self.text6.insert(INSERT, '结果：成功\n')
                    self.text6.insert(INSERT, '详情：' + str(json.loads(res.read())) + '\n')
                else:
                    # 请求成功，背景为绿色；失败则为红色
                    self.text6 = Text(self.frame2, bg='red')
                    self.text6.pack(fill=BOTH)
                    self.text6.insert(INSERT, self.vChoose.get() + '\n')
                    self.text6.insert(INSERT, '结果：失败\n')
            else:
                showwarning(message='*标记的内容均不能为空！')
        # 用于请求积分查询
        if '积分查询' == self.vChoose.get():
            if '' != self.vuid.get():
                conn_http = httplib.HTTPConnection(self.hosturl)
                conn_http.request('GET', '/points/' + self.vuid.get(), '', self.dic_header)
                res = conn_http.getresponse()
                if res.status == 200 or res.status == 201:
                    # 请求成功，背景为绿色；失败则为红色
                    dict_body = json.loads(res.read())
                    self.text6 = Text(self.frame2, bg='green')
                    self.text6.pack(fill=BOTH)
                    self.text6.insert(INSERT, self.vChoose.get() + '\n')
                    self.text6.insert(INSERT, '结果：成功\n')
                    self.text6.insert(INSERT, '姓名：' + dict_body['first_name'] + dict_body['last_name'] + '\n')
                    self.text6.insert(INSERT, '当前积分：' + str(dict_body['points']) + '\n')
                    self.text6.insert(INSERT, '签到状态：' + str(dict_body['visa_checkin_enabled']) + '\n')
                    self.text6.insert(INSERT, '兑现比例：' + str(dict_body['points_conversion_rate']) + '%' + '\n')
                else:
                    # 请求成功，背景为绿色；失败则为红色
                    self.text6 = Text(self.frame2, bg='red')
                    self.text6.pack(fill=BOTH)
                    self.text6.insert(INSERT, self.vChoose.get()+'\n')
                    self.text6.insert(INSERT, '结果：失败\n')
                    self.text6.insert(INSERT, '原因：IMEI编号不存在\n')
            else:
                showwarning(message='*标记的内容均不能为空！')

    # 用于隐藏控件，方便重新布局
    def forgetAll(self):
        for i in [self.label1, self.label2, self.label3, self.label4, self.label5, self.label6,
            self.label7, self.label8, self.label9,
            self.label10, self.label11, self.label12,
            self.label13, self.label14, self.button1, self.button2,
            self.text1, self.text2, self.text3, self.text4, self.text5, self.text6]:
            i.grid_forget()
        self.text6.pack_forget()

    # 用于清空控件内容
    def clearAll(self):
        for i in [self.vfirst_name, self.vlast_name, self.vphone, self.vuid, self.vemail]:
            try:
                i.set('')
            except:
                pass
        self.text6.pack_forget()
       
if __name__ == '__main__':
    myframe = MyFrame()
    mainloop()