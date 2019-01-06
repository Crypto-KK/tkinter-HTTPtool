import tkinter as tk
import requests
from tkinter import scrolledtext
import re
from tkinter import messagebox
from lxml import etree
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.create_menubar()
    def create_widgets(self):
        #bar
        self.canvas = tk.Canvas(self,width=980,height=65,bg='#ebf4ec')
        self.image_file = tk.PhotoImage(file='network.png')
        self.imag = self.canvas.create_image(50,0,anchor='n',image=self.image_file)
        self.canvas.create_text(480,35,text='HTTP测试工具',font=('Arial',35),)
        self.canvas.grid(row=0,columnspan=3)

        #method
        self.var_method = tk.StringVar(self)
        self.var_method.set('GET')
        self.optionmenu = tk.OptionMenu(self,self.var_method,'GET','POST','PUT','PATCH','DELETE','HEAD','OPTIONS').grid(row=1,column=0,padx=2,pady=2,ipadx=10,ipady=5)

        #url
        self.var_url = tk.StringVar(self)
        self.var_url.set('http://193.112.41.211:5000')
        self.url_entry = tk.Entry(self,font=('Arial',14),width=82,textvariable=self.var_url).grid(row=1,column=1,padx=1,pady=2,ipadx=10,ipady=5)

        #request button
        self.request_button = tk.Button(self, text='发送请求', fg='#436EEE', command=self.request).grid(row=1,column=2,padx=2,pady=2,ipadx=10,ipady=5)

        #request header
        self.header_label = tk.Label(self,text='请求头：').grid(row=3,column=0,padx=2,pady=2,ipadx=10,ipady=5)
        self.var_header = tk.StringVar(self)
        self.var_header.set('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:64.0) Gecko/20100101 Firefox/64.0')
        self.header_entry = tk.Entry(self,font=('Arial',14),width=82,textvariable=self.var_header).grid(row=3,column=1,padx=2,pady=2,ipadx=10,ipady=5)

        #regular expression
        self.re_header = tk.Label(self,text='正则表达式：').grid(row=4,column=0,padx=2,pady=2,ipadx=10,ipady=5)
        self.var_re = tk.StringVar(self)
        self.re_entry = tk.Entry(self,font=('Arial',14),width=82,textvariable=self.var_re).grid(row=4,column=1,padx=2,pady=2,ipadx=10,ipady=5)
        self.re_button = tk.Button(self, text='匹配全部',command=self.re_request).grid(row=4,column=2,padx=2,pady=2,ipadx=10,ipady=5)


        #xpath
        self.xpath_label = tk.Label(self,text='Xpath表达式：').grid(row=5,column=0,padx=2,pady=2,ipadx=10,ipady=5)
        self.var_xpath = tk.StringVar(self)
        self.xpath_entry = tk.Entry(self,font=('Arial',14),width=82,textvariable=self.var_xpath).grid(row=5,column=1,padx=2,pady=2,ipadx=10,ipady=5)
        self.xpath_button = tk.Button(self, text='匹配全部',command=self.xpath_request).grid(row=5,column=2,padx=2,pady=2,ipadx=10,ipady=5)


        #information
        self.var_status = tk.StringVar()
        self.var_status.set('当前状态：未请求')
        self.information = tk.Label(self,textvariable=self.var_status,bg='#48D1CC',font=('Arial',14)).grid(row=6, column=1, padx=2, pady=2, ipadx=10, ipady=5)


        #results
        self.textarea = tk.scrolledtext.ScrolledText(self,width=117,height=25,bg='black',fg='#00EE00',font=('Arial',14))
        self.textarea.grid(row=7,columnspan=3,pady=10)


    def create_menubar(self):
        pass


    def xpath_request(self):
        xpath = self.var_xpath.get()
        if xpath == '':
            messagebox.showinfo('警告', message='请输入XPATH表达式！')
        else:
            url = self.var_url.get()
            header = self.var_header.get()
            headers = {'User-Agent':header}
            data = requests.get(url=url,headers=headers).text
            results = etree.HTML(data).xpath(xpath)
            self.textarea.delete('1.0', 'end')
            for i in results:

                self.textarea.insert('end',i.text + '\n')

    #正则表达式匹配
    def re_request(self):
        exp = self.var_re.get()
        if exp == '':
            messagebox.showinfo('警告',message='请输入正则表达式！')
        else:
            url = self.var_url.get()
            header = self.var_header.get()
            headers = {'User-Agent':header}
            data = requests.get(url=url,headers=headers).text
            results = re.compile(exp).findall(data)
            self.textarea.delete('1.0', 'end')
            self.textarea.insert('end',results)

    def request(self):
        method = self.var_method.get()
        if method == 'GET':
            self.get_request()
        elif method == 'POST':
            self.post_request()


    def post_request(self):
        pass

    #发送HTTP GET请求
    def get_request(self):
        self.textarea.delete('1.0','end')
        if self.var_header.get() == '':
            headers = {'User-Agent':''}
        else:
            headers = {'User-Agent':self.var_header.get()}
        url = self.var_url.get()

        data = requests.get(url=url,headers=headers)
        if (data.status_code == 200):
            self.var_status.set('当前状态：'+ 'GET ' + url + '    '+ str(data.status_code)+' OK')

        elif (data.status_code == 404):
            self.var_status.set('当前状态：' + str(data.status_code) + ' Not found')
        else:
            self.var_status.set('当前状态：' + str(data.status_code))
        content = data.text
        self.textarea.insert('end',content)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('KK HTTP测试工具')
    root.geometry('980x700')
    #root.resizable(width=False,height=False)
    app = Application(master=root)
    app.mainloop()