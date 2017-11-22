#coding=utf-8
#日期：20170619
#开发者： 杨过展昭 728074993@qq.com
#文本文件修改程序：淘宝客户
from Tkinter import *
from collections import OrderedDict
import tkMessageBox
import os
import logging

logging.basicConfig(level=logging.ERROR)
#from ttk import *
class MainPage(Frame):
	"""
	tester UI With Tkinter
	接口见config定义
	"""
	def __init__(self, parent, root):
		Frame.__init__(self, parent)
		self.value=OrderedDict()
		self.filePath=""
		self.createWidgets()
	def createWidgets(self):
		config=OrderedDict([
			("呼号001",""),
			("双工003",["开","关"]),
			("接收频率011",""),
			("发射频率012",""),
			("功率013",""),
			("CW029",["开","关"]),
			("CW时间030",""),
			("PTT点平042",["高","低"]),

			("DMR068",["开","关"]),
			("信标069",["开","关"]),
			("色码071",""),
			("网络099",["开","关"]),
			("网络组103",""),
			("时隙1106",["开","关"]),
			("时隙2107",["开","关"]),

			("P25087",["开","关"]),
			("网络码088",""),
			("网络119",["开","关"]),
			("网络组122",""),

			("D-Star062",["开","关"]),
			("网络092",["开","关"]),
			("本地端口095",""),

			("C4FM082",["开","关"]),
			("网络111",["开","关"]),
			("本地IP112",""),
			("本地端口113",""),
			("网关IP114",""),
			("网关端口115",""), 
			])
		rowWidth = 10
		rowHeight = 3
		row=0
		num=0
		chanel=[7,6,3,2,5]
		for item in config:
			Label(self,text=item[:-3],width=7,anchor="e").grid(row=row,column=2*(num%2),sticky="we")
			self.value[item]=StringVar()
			if config[item]:
				self.value[item].set("")
				OptionMenu(self,self.value[item],*config[item]).grid(row=row,column=2*(num%2)+1,sticky="w")
			else:
				self.value[item].set("")
				Entry(self,text=self.value[item]).grid(row=row,column=2*(num%2)+1,sticky="we")
			
			if num%2==1:
				row +=1
			if num == chanel[0]:
				chanel.pop(0)
				num=-1
				row +=1
				Label(self,text="_"*100,width=rowWidth).grid(row=row,column=0,columnspan=4,sticky="we")
				row +=1
			num +=1
		Button(self,text="读取",command=self.selectPath).grid(row=row,column=0,columnspan=2,sticky="we")
		Button(self,text="写入",command=self.run).grid(row=row,column=2,columnspan=2,sticky="we")
		row=row+1
		Button(self,text="PI重启",command=self.reboot).grid(row=row,column=0,sticky="we")
		Button(self,text="ID管理",command=self.openFile).grid(row=row,column=1,sticky="we")
		Button(self,text="启动",command=self.start).grid(row=row,column=2,sticky="we")
		Button(self,text="关闭",command=self.stop).grid(row=row,column=3,sticky="we")

	def selectPath(self):
		if os.path.exists("/home/pi/MMDVM.ini"):
			path = "/home/pi/MMDVM.ini"
			self.filePath=path
		else:
			tkMessageBox.showinfo("错误提示", "/home/pi/MMDVM.ini不存在")

	def reboot(self):
		os.system('sudo reboot')

	def run(self):
		try:
			f=open(self.filePath,'r')
			lines=f.readlines()
			for item in self.value:
				#print item[:-3],'=',self.value[item].get()
				#print lines[int(item[-3:])]
				#print '='*20
				value=""
				if self.value[item].get()=="":
					value=lines[int(item[-3:])].split("=")[1][:-1]
					#print value
				elif self.value[item].get()==u"开" or self.value[item].get()==u"高":
					value="1"
					#print value
				elif self.value[item].get()==u"关" or self.value[item].get()==u"低":
					value="0"
					#print value
				else:
					value=self.value[item].get()
					#print value
				logging.info(lines[int(item[-3:])].split("=")[0])
				lines[int(item[-3:])]=lines[int(item[-3:])].split("=")[0]+'='+value+'\n'
			#print lines
			ff=open(self.filePath,'w')
			ff.writelines(lines)
			ff.close()
		except Exception as e:
			pass
			logging.info(e)
		
	def openFile(self):
		os.system("geany /home/pi/Applications/MMDVMHost/DMRIds.dat")
	def start(self):
		os.system("sudo chmod +x /usr/share/applications/MMDVMHost Background Service")
		os.system("/usr/share/applications/MMDVMHost Background Service")
	def stop(self):
		os.system("sudo chmod +x /usr/share/applications/MMDVMHost Background Service")
		os.system("/usr/share/applications/MMDVMHost Background Service")

if __name__ == '__main__':
	root=Tk()
	#root.attributes("-fullscreen", True)
	root.geometry('450x600') #官方7寸显示屏大小
	root.wm_title("中继参数修改by天津小志")

	# 修改默认字体大小
	import tkFont
	#default_font = tkFont.nametofont("TkDefaultFont")
	#default_font.configure(size=12)
	#root.option_add("*Font", default_font)
	
	container = Frame(root)
	page = MainPage(root,container)
	page.grid(row=0, column=0, sticky="nsew")
	
	from datetime import datetime
	import threading
	import time

	def rebootAt24():
		while(1):
			timeNow=datetime.now().strftime('%H:%M')
			if timeNow=="24:00":
				os.system('sudo reboot')
			time.sleep(50)
	threadReboot = threading.Thread(target=rebootAt24)
	threadReboot.setDaemon(True)
	threadReboot.start()
	
	
	#[x]关闭窗口
	def closeWindow():
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', closeWindow)
	root.mainloop()
