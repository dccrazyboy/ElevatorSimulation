#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 

'''
from ElevatorSimulation import ElevatorSimulation
import wx
import time
import thread

class GuiFrame(wx.Frame):
	''' 窗体显示类 
		
		@ivar simu: 模拟类
		@type simu: ElevatorSimulation
		
		@ivar EleInfo: 电梯信息显示控件
		@type EleInfo: list
		
		@ivar FloorInfo: 楼层信息显示控件
		@type FloorInfo: list
		
		@ivar SimuInfo: 模拟控制信息显示控件
		@type SimuInfo: wx.StaticText
	'''
	def __init__(self,simu):

		''' 初始化电梯信息 
			@type simu: ElevatorSimulation
			@param simu: 模拟类
	   '''
		self.simu = simu
		
		wx.Frame.__init__(self, None, -1, u'电梯模拟',size=(1200, 750))
		panel = wx.Panel(self) #创建画板

		self.EleInfo = []
		self.FloorInfo = []
		self.SimuInfo = None
		# 当前模拟情况控件
		self.SimuInfo = wx.StaticText(panel, -1, u"当前状态：" , pos=(10, 10))
		# 电梯信息显示控件
		for i in range(10):
			self.EleInfo.append(wx.StaticText(panel, -1, self.simu.elevatorCtl.AllElevator[i].Tag , pos=(10, 50 + i * 65)))
			#self.EleInfo[-1].SetBackgroundColour('black')
			#self.EleInfo[-1].SetForegroundColour('white')
		# 楼层信息显示控件
		for i in range(4):
			for j in range(10):
				self.FloorInfo.append(wx.StaticText(panel, -1, u"楼层 " + str(i * 10 + j + 1) , pos=(180 + j * 100, 50 + i * 150)))

		#self.__update()
		thread.start_new_thread(self.__update,())



	def __update(self):
		''' 时间+1并更新全部信息 '''
		while (True):
			ret = self.simu.AddTimer()
			self.__updateSimuInfo(ret)
			self.__updateEleInfo(ret)
			self.__updateFloorInfo(ret)
			
			if ret == 'Finish':
				self.__updateInRequestTime()
				break
			time.sleep(1)

	def __formatEleInfo(self,ele,ret):
		''' 格式化电梯信息 
			@type ele: Elevator
			@param ele: 电梯对象
		
			@type ret: str
			@param ret: 当前返回的状态
		'''
		Tag,Status,NowFloor,CustomerList,RequsetList,IdleTime,RunningTime = ele.GetNowStatus()
		if ret !='Finish':
			eleInfo = Tag + '\n' + \
					  u"状态：" + Status + ' ' + u"楼层：" + str(NowFloor) + '\n' + \
					  u"当前电梯内顾客数：" + str(len(CustomerList)) + '\n' + \
					  u"顾客ID:"
			for cust in CustomerList:
				eleInfo += str(cust.ID) + ','
		else:
			eleInfo = Tag + '\n' + \
					  u"状态：" + Status + ' ' + u"楼层：" + str(NowFloor) + '\n' + \
					  u"运行时间：" + str(RunningTime) + '\n' + \
					  u"空闲时间：" + str(IdleTime)
		return eleInfo
	
	def __updateEleInfo(self,ret):
		''' 更新电梯信息 
			@type ret: str
			@param ret: 当前返回的状态
		'''
		for i in range(10):
			self.EleInfo[i].SetLabel(self.__formatEleInfo(self.simu.elevatorCtl.AllElevator[i],ret))


	def __formatSimuInfo(self,ret):
		''' 格式化模拟系统信息 
			@type ret: str
			@param ret: 当前返回的状态
		'''
		if ret != 'Finish':
			SimuInfo = u"模拟中，模拟时间：" + str(self.simu.timer.GetNowTime())
		else:
			SimuInfo = u"模拟结束，模拟时间：" + str(self.simu.timer.GetNowTime())
		return SimuInfo
	
	def __updateSimuInfo(self,ret):
		''' 更新模拟系统信息 
			@type ret: str
			@param ret: 当前返回的状态
		'''
		self.SimuInfo.SetLabel(self.__formatSimuInfo(ret))


	def __formatFloorInfo(self,floorView,floor,ret):
		''' 格式化模拟系统信息 
			@type floorView: FloorView
			@param floorView: 楼层显示类

			@type floor: int
			@param floor: 楼层
			
			@type ret: str
			@param ret: 当前返回的状态
		'''

		if ret != 'Finish':
			WaitingCustomer,InRequestCustomer = floorView.GetFloorInfo(floor)
			FloorInfo = u"楼层：" + str(floor) + u'\n' + \
						u"等待电梯顾客：\n"
			for cust in InRequestCustomer:
				FloorInfo += u"(%d-%d) " % (cust.ID,cust.DestFloor)
			FloorInfo += u'\n'
			FloorInfo += u"闲置顾客ID：\n"
			for cust in WaitingCustomer:
				FloorInfo += str(cust.ID) + u','
		else:
			FloorInfo = ""
		return FloorInfo
	
	def __updateFloorInfo(self,ret):
		''' 更新楼层信息 
			@type ret: str
			@param ret: 当前返回的状态
		'''
		for i in range(40):
			self.FloorInfo[i].SetLabel(self.__formatFloorInfo(self.simu.floorView,i+1,ret))
			self.FloorInfo[i].Wrap(95)
			
	def __updateInRequestTime(self):
		''' 更新用户等待时间
		'''
		AllInRequestTime = self.simu.customerCtl.GetAllInRequestTime()
		InRequest = u"用户等待电梯事件(ID-Time)：\n"
		for ID in AllInRequestTime:
			InRequest += "(%d-%d) " % (ID,AllInRequestTime[ID])
		self.FloorInfo[0].SetLabel(InRequest)
		self.FloorInfo[0].Wrap(1000)
			
	def OnCloseWindow(self, event):
		''' 窗体销毁 
		'''
		self.Destroy()

def gui():
	simu = ElevatorSimulation(10,10,1,1,2,False)
	app = wx.PySimpleApp()
	frame = GuiFrame(simu)
	frame.Show()
	app.MainLoop()

	
if __name__ == '__main__':


	import cProfile
	cProfile.run("gui()", "result")
	import pstats
	p = pstats.Stats("result")
	p.sort_stats("time").print_stats()



