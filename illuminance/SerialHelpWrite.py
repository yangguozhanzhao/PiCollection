# coding=utf-8

'''
Serial设备通讯帮助类
'''

import sys
import threading
import time
import serial
import binascii
import logging

class SerialHelper(object):
	data = ''
	def __init__(self, Port, BaudRate="9600", ByteSize="8", Parity="N", Stopbits="1"):
		'''
		初始化一些参数
		'''
		self.write_serial = None
		self.alive = False
		self.port = Port
		self.baudrate = BaudRate
		self.bytesize = ByteSize
		self.parity = Parity
		self.stopbits = Stopbits
		
		
		self.thresholdValue = 16
		self.receive_data = ""
		
	def start(self):
		'''
		开始，打开串口
		'''
		self.write_serial = serial.Serial()
		self.write_serial.port = self.port
		self.write_serial.baudrate = self.baudrate
		self.write_serial.bytesize = int(self.bytesize)
		self.write_serial.parity = self.parity
		self.write_serial.stopbits = int(self.stopbits)
		self.write_serial.timeout = 1
		self.write_serial.interCharTimeout = 0.3

		try:
			self.write_serial.open()
			if self.write_serial.isOpen():
				self.alive = True
		except Exception as e:
			self.alive = False
			logging.error(e)

	def stop(self):
		'''
		结束，关闭串口
		'''
		self.alive = False
		if self.write_serial.isOpen():
			self.write_serial.close()

	def read(self):
		'''
		循环读取串口发送的数据
		'''
		while self.alive:
			try:
				number = self.write_serial.inWaiting()
				if number:
					self.receive_data += self.write_serial.read(number)
					if self.thresholdValue < len(self.receive_data):
						self.receive_data = ""
					else:                        
						self.receive_data = str(binascii.b2a_hex(self.receive_data))
						self.__class__.data = self.receive_data
						print self.__class__
						print self.receive_data
			except Exception as e:
				logging.error(e)

	def write(self, data, isHex=False):
		'''
		发送数据给串口设备
		'''
		if self.alive:
			if self.write_serial.isOpen():
				if isHex:
					data = binascii.unhexlify(data)
				self.write_serial.write(data)
				
if __name__ == '__main__':
	import threading
	#ser = SerialHelper("COM5")
	ser = SerialHelper("/dev/ttyUSB0")
	
	ser.start()
	now=time.strftime('%Y-%m-%d %X',time.localtime())
	num = "1234567"
	print(num[0:5], type(now))
	ser.write("1234567" + "\n")
