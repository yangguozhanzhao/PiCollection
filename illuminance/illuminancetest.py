# encoding: utf-8
import smbus
import time
import SerialHelpWrite

#BH1750地址
__DEV_ADDR=0x23

#光照模块控制字
__CMD_PWR_OFF=0x00  #关机
__CMD_PWR_ON=0x01   #开机
__CMD_RESET=0x07    #重置

__CMD_THRES2=0x21   #一次高分辨率模式2

__CMD_SEN100H=0x42  #灵敏度100%,高位
__CMD_SEN100L=0X65  #灵敏度100%，低位


bus=smbus.SMBus(1)
bus.write_byte(__DEV_ADDR,__CMD_PWR_ON)
bus.write_byte(__DEV_ADDR,__CMD_RESET)
bus.write_byte(__DEV_ADDR,__CMD_SEN100H)
bus.write_byte(__DEV_ADDR,__CMD_SEN100L)
bus.write_byte(__DEV_ADDR,__CMD_PWR_OFF)
def getIlluminance():
    bus.write_byte(__DEV_ADDR,__CMD_PWR_ON)
    bus.write_byte(__DEV_ADDR,__CMD_THRES2)
    time.sleep(0.2)
    res=bus.read_word_data(__DEV_ADDR,0)
    #read_word_data
    res=((res>>8)&0xff)|(res<<8)&0xff00
    res=round(res/(2*1.2),2) #此处的照度单位为lx
    return str(res)

# 将数据写入illuminance.csv
while 1:
	import threading
	ser = SerialHelpWrite.SerialHelper("/dev/ttyUSB0")
	ser.start()
	lx=getIlluminance()
	now = time.strftime('%Y-%m-%d %X',time.localtime())
	lxstr = str(lx)
	str_temp = lxstr + " " + now
	str_length = len(str_temp)
	print(str_length)
	for i in range(0, 5):
		try:
			ser.write(str_temp[6*i:6*(i+1)])
		except:
			pass
	ser.write("\n")
	time.sleep(10*60) #每十分钟读取一次

