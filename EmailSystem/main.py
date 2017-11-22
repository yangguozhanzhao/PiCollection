#!/usr/bin/env
# coding=utf-8
# Copyright By Yangzhan 20170401
import Tkinter as tk
import tkFont
import RPi.GPIO as GPIO
import tkMessageBox
import pygame
from PIL import Image, ImageTk 
import emailConfig
import os
import subprocess


class bgFrame(tk.Frame):
	def __init__(self,master,im):
		tk.Frame.__init__(self,master)
		helv16 = tkFont.Font(family='Helvetica',size=6, weight='bold')
		self.canvas = tk.Canvas(self, width = 1920,height = 1080,bg = 'white')
		self.canvas.create_image(1920/2,1080/2,image = im)
		self.canvas.create_text(100,20, text = '邮件系统 V0.1', fill = 'white') 
		self.canvas.grid(row = 0, column = 0, padx=0,pady=0,sticky = "nwse")
		

class App(tk.Frame):
	def __init__(self,master,bg=""):
		tk.Frame.__init__(self, master)

		
		#锁的PIN针
		self.lockPin = 31
		GPIO.setup(self.lockPin,GPIO.OUT,initial=1)
		GPIO.setup(29,GPIO.OUT,initial=0)
		
		#密码
		self.lockCode=emailConfig.LOCKCODE
		self.settingCode=emailConfig.SETTINGCODE
		
		#声音
		pygame.init()
		pygame.mixer.init()
		self.soundwav=pygame.mixer.Sound("开门声.wav") 
		
		image_file = Image.open("bg.jpg")  
		self.im = ImageTk.PhotoImage(image_file) 
		
		image = Image.open("close.png")  
		self.imClose = ImageTk.PhotoImage(image) 
		
		image = Image.open("receiver.png")  
		self.imReceiver = ImageTk.PhotoImage(image) 
		
		image = Image.open("send.png")  
		self.imSend = ImageTk.PhotoImage(image) 
		
		self.helv36 = tkFont.Font(family='Helvetica',size=36, weight='bold')
		
		self.recipient=emailConfig.RECIPIENT
		self.send=emailConfig.SEND
		
		self.createLoginFrame()
		self.createEmailFrame() 
		self.createSettingFrame()
		self.loginFrame.tkraise()
		
		
	def createLoginFrame(self):
		self.loginFrame = bgFrame(self,self.im)
		
		
		self.loginFrame.canvas.create_text(960,200, text = '登录邮件系统', fill = 'white',font=self.helv36)
		
		helv20 = tkFont.Font(family='Helvetica',size=25, weight='bold')
		
		self.loginFrame.canvas.create_text(640,400, text = '输入密码', fill = 'white',font=helv20) 
		
		self.codeArea = tk.StringVar() 
		code = tk.Entry(self.loginFrame.canvas,show = '*',textvariable = self.codeArea,font=helv20)
		self.loginFrame.canvas.create_window( 960,400,window=code)
		
		loginButton = tk.Button(self.loginFrame.canvas,text="登录",command=self.login,font=helv20)
		self.loginFrame.canvas.create_window( 1250,400,tags='BTN1',window=loginButton)
		
		self.loginFrame.grid(row=0, column=0, sticky="nsew",padx=0,pady=0)	

	def createEmailFrame(self):
		self.emailFrame = bgFrame(self,self.im)
		self.emailFrame.canvas.create_text(960,50, text = '邮箱', fill = 'white',font=self.helv36)
		self.emailFrame.canvas.create_line(0,80,1920,80,width=2,fill = 'white')
		self.emailFrame.canvas.create_line(180,80,180,1080,width=2,fill = 'white')
		self.emailFrame.canvas.create_line(0,0,0,1080,width=2,fill = 'white')
		self.emailFrame.canvas.create_line(0,1080,1920,1080,width=2,fill = 'white')
		self.emailFrame.canvas.create_line(1920,1080,1920,0,width=2,fill = 'white')

		backButton = tk.Button(self.emailFrame.canvas,text="",command=self.backLogin,image=self.imClose,bg="white",relief=tk.FLAT)
		self.emailFrame.canvas.create_window( 1850,26,window=backButton)
		
		label1 = tk.Label(self.emailFrame.canvas,image=self.imReceiver,bg="white")
		self.emailFrame.canvas.create_window( 50,120,window=label1)
		self.emailFrame.canvas.create_text(100,120, text = '收件箱', fill = 'white')
		
		y=180
		for key in self.recipient:
			button = tk.Button(self.emailFrame,text=self.recipient[key]["subject"],bg="white",anchor="w",relief=tk.FLAT,command=lambda email=self.recipient[key]:self.showEmail(email))
			self.emailFrame.canvas.create_window(50,y,window=button,width=120,anchor = 'w')
			y+=50
		
		label2 = tk.Label(self.emailFrame.canvas,image=self.imSend,bg="white")
		self.emailFrame.canvas.create_window( 50,500,window=label2)
		self.emailFrame.canvas.create_text(100,500, text = '已发送', fill = 'white')
		
		y=560
		for key in self.send:
			button = tk.Button(self.emailFrame,text=self.send[key]["subject"],bg="white",anchor="w",relief=tk.FLAT,command=lambda email=self.send[key]:self.showEmail(email))
			self.emailFrame.canvas.create_window(50,y,window=button,width=120,anchor = 'w')
			y+=50
		
		self.subjectText=self.emailFrame.canvas.create_text(220,120,text ="主题："+ self.recipient["one"]["subject"], fill = 'white',anchor="w")
		self.senderText=self.emailFrame.canvas.create_text(220,150,text = "发件人："+self.recipient["one"]["sender"], fill = 'white',anchor="w")
		self.timeText=self.emailFrame.canvas.create_text(220,180,text =  "时间："+self.recipient["one"]["time"], fill = 'white',anchor="w")
		self.recipientText=self.emailFrame.canvas.create_text(220,210,text ="收件人："+ self.recipient["one"]["recipient"], fill = 'white',anchor="w")
		self.contentText = tk.Text(self.emailFrame,height=32,width=138)
		#音频
		if self.recipient["one"]["audio"]!="":
			button = tk.Button(self.contentText,text="播放"+self.recipient["one"]["audio"],command=lambda audio=self.recipient["one"]["audio"]:self.palyAudio(audio))
			self.contentText.window_create(tk.INSERT,window=button)
		
		#视频
		if self.recipient["one"]["vedio"]!="":
			button = tk.Button(self.contentText,text="播放"+self.recipient["one"]["vedio"],command=lambda vedio=self.recipient["one"]["vedio"]:self.playVedio(vedio))
			self.contentText.window_create(tk.INSERT,window=button)
		
		self.contentText.insert(tk.INSERT,self.recipient["one"]["content"])
		self.emailFrame.canvas.create_window( 220,240,window=self.contentText,anchor = "nw")
		
		image = Image.open(self.recipient["one"]["image"])  
		self.cimage = ImageTk.PhotoImage(image) 
		self.contentImage=self.contentText.image_create(tk.INSERT,image=self.cimage)
		
		self.contentText.config(state="disabled")
		self.emailFrame.grid(row=0, column=0,sticky="nsew",padx=0,pady=0)
	
	def createSettingFrame(self):
		self.settingFrame = bgFrame(self,self.im)
		self.settingFrame.canvas.create_text(960,300,text = '密码长度小于20位，可以数字字母组合，字母区分大小写', fill = 'white',anchor = 'center')
		
		self.settingFrame.canvas.create_text(780,400, text = '输入密码', fill = 'white')
		self.newCode = tk.StringVar()
		code1 = tk.Entry(self.settingFrame.canvas,show = '*',textvariable = self.newCode)
		self.settingFrame.canvas.create_window( 960,400,window=code1)

		self.settingFrame.canvas.create_text(780,450, text = '确认密码', fill = 'white')
		self.confirmCode = tk.StringVar()
		code2 = tk.Entry(self.settingFrame,show = '*',textvariable = self.confirmCode)
		self.settingFrame.canvas.create_window( 960,450,window=code2)

		confirmButton = tk.Button(self.settingFrame.canvas,text="确认修改",command=self.updateCode)
		self.settingFrame.canvas.create_window( 890,500,window=confirmButton)
		
		backButton = tk.Button(self.settingFrame.canvas,text="返回",command=self.backLogin)
		self.settingFrame.canvas.create_window( 1050,500,window=backButton)

		self.settingFrame.grid(row=0, column=0, sticky="nsew")

	
	def login(self):
		inputCode = self.codeArea.get()
		print inputCode

		if inputCode == self.settingCode:
			self.setting()
		elif inputCode == self.lockCode:
			self.unlock()
		else:
			self.lock()
			tkMessageBox.showinfo("错误提示", "密码错误")
			
	def unlock(self):
		print "开锁"
		self.codeArea.set("")
		GPIO.output(self.lockPin, 0)
		self.emailFrame.tkraise()
		self.soundwav.play()
		
	def lock(self):
		print "锁定"
		self.codeArea.set("")
		GPIO.output(self.lockPin, 1)
		
	
	def setting(self):
		self.settingFrame.tkraise()
		print "设置"
	
	def updateCode(self):
		self.codeArea.set("")
		newCode = self.newCode.get()
		confirmCode = self.confirmCode.get()
		if len(newCode)>20:
			tkMessageBox.showinfo("密码设置提示", "密码长度超过20字符")
		elif newCode==self.settingCode:
			tkMessageBox.showinfo("密码设置提示", "解锁密码与设置密码不能相同")
		elif len(newCode)<6:
			tkMessageBox.showinfo("密码设置提示", "密码长度不够")
		elif newCode == confirmCode:
			tkMessageBox.showinfo("密码设置提示", "解锁密码设置成功")
			
			filename='emailConfig.py'
			lines=[]
			f=open(filename,'r')
			lines=f.readlines()
			print lines[2]
			lines[2]='LOCKCODE=\"'+newCode+'\"\n'
			f=open(filename,'w')
			f.writelines(lines)
			f.close()
			self.lockCode=newCode
			
			self.loginFrame.tkraise()
		else:
			tkMessageBox.showinfo("密码设置提示", "两次输入密码不一致")

	def backLogin(self):
		pygame.mixer.stop()
		os.system("pkill omxplayer")
		self.lock()
		self.loginFrame.tkraise()
		
	def playVedio(self,vedio):
		pygame.mixer.stop()
		subprocess.Popen(["omxplayer",vedio])
	
	def palyAudio(self,audio):
		pygame.mixer.stop()
		os.system("pkill omxplayer")
		self.audio=pygame.mixer.Sound(audio)
		self.audio.play()
	
	def showEmail(self,email):
		self.contentText.config(state="normal")
		self.emailFrame.canvas.itemconfigure(self.subjectText, text="主题："+email["subject"])
		self.emailFrame.canvas.itemconfigure(self.senderText, text="发件人："+email["sender"])
		self.emailFrame.canvas.itemconfigure(self.timeText, text="时间："+email["time"])
		self.emailFrame.canvas.itemconfigure(self.recipientText, text="收件人："+email["recipient"])
		self.contentText.delete(1.0,tk.END)
		pygame.mixer.stop()
		if email["audio"] !="": 
			button = tk.Button(self.contentText,text="播放"+email["audio"],command=lambda audio=email["audio"]:self.palyAudio(audio))
			self.contentText.window_create(tk.INSERT,window=button)
		if email["vedio"]!="":
			button = tk.Button(self.contentText,text="播放"+email["vedio"],command=lambda vedio=email["vedio"]:self.playVedio(vedio))
			self.contentText.window_create(tk.INSERT,window=button)
			
		self.contentText.insert(tk.INSERT,email["content"])
		
		if email["image"] !="":
			image = Image.open(email["image"])  
			self.cimage = ImageTk.PhotoImage(image) 
			self.contentImage=self.contentText.image_create(tk.INSERT,image=self.cimage)
		self.contentText.config(state="disabled")

if __name__ == '__main__':
	import socket 
	import sys
	hostname = socket.gethostname()
	if hostname != "oczjyangxc":
		exit()
	os.chdir(sys.path[0]) 
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	root=tk.Tk()
	root.wm_title("邮件系统")
	root.geometry('1920x1080') 
	# 修改默认字体大小
	default_font = tkFont.nametofont("TkDefaultFont")
	default_font.configure(size=15)
	root.option_add("*Font", default_font)
	root.attributes("-fullscreen", True)
	
	def escape(event):
		os.system("pkill omxplayer")
	root.bind("<Escape>",escape)
	app = App(root)
	app.pack()	
	
	def closeWindow():
		app.lock()
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', closeWindow)
	root.mainloop()
