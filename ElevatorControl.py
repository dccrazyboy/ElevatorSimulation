#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 

'''
from Elevator import Elevator
import random
#from Logger import Logger

class ElevatorControl(object):
	""" 电梯控制类，控制所有电梯运行 
		
		@ivar AllElevator: 所有电梯列表
		@type AllElevator: Elevator
	"""
	def __init__(self,MaxCustomer,Speed,BoardTime):
		''' 初始化 
			@type MaxCustomer: int
			@param MaxCustomer: 每部电梯最大顾客数
		
			@type Speed: int
			@param Speed: 电梯运行速度 Speed秒/层
			
			@type BoardTime: int
			@param BoardTime: 顾客上下电梯耗时
		'''
		self.AllElevator = []
		
		# 电梯基本信息
		AvaliableFloorTable = {
			'E0' : range(1,41),
			'E1' : range(1,41),
			'E2' : [1] + range(25,41),
			'E3' : [1] + range(25,41),
			'E4' : range(1,26),
			'E5' : range(1,26),
			'E6' : [1] + range(2,41,2),
			'E7' : [1] + range(2,41,2),
			'E8' : range(1,41,2),
			'E9' : range(1,41,2)
			}
		ElevatorNum = len(AvaliableFloorTable)

		# 产生电梯
		for tag,floor in AvaliableFloorTable.items():
			newElevator = Elevator(tag,floor,MaxCustomer,random.choice(floor),Speed,BoardTime)
			self.AllElevator.append(newElevator)
			#print newElevator

		self.AllElevator.sort(cmp = lambda x,y: cmp(x.Tag, y.Tag))
		
		#for elevator in self.AllElevator:
		#	 print str(elevator) + '\n'

	def __str__(self):
		''' 打印电梯控制类信息 '''
		printStr = '[ElevatorControl] \n'
		#for elevator in self.AllElevator:
		#	 if elevator.Status != 'Idle':
		#		 printStr = printStr + str(elevator) + '\n'

		count = 0
		for elevator in self.AllElevator:
			if elevator.Status != 'Idle':
				count = count + 1
		printStr = printStr + 'Not Idle Elevator = %d' % count
		return printStr
	
	def AddTimer(self,NowTime):
		''' 调用此函数通知时间加1，更新内部状态
			@type NowTime: int
			@param NowTime: 当前时间，一般不做使用
		'''
		# 通知所有Elevator的Timer加1
		for elevator in self.AllElevator:
			elevator.AddTimer(NowTime)

	def GetBestElevator(self,customer):
		''' 通过customer信息获得最优电梯 
			@type customer: Customer
			@param customer: 顾客对象
		
			@rtype: Elevator
			@return: 分配到的电梯
		'''
		
		# 找出可用电梯
		AvaliableElevator = []
		for ele in self.AllElevator:
			if len(ele.CustomerList) + len(ele.RequsetList) < ele.MaxCustomer \
			   and customer.NowFloor in ele.AvaliableFloor \
			   and customer.DestFloor in ele.AvaliableFloor:
				AvaliableElevator.append(ele)

				
		# 查找空闲电梯
		Distance = []
		for elevator in AvaliableElevator:
			if elevator.Status == 'Idle':
				Distance.append(abs(elevator.NowFloor - customer.NowFloor))
		#print 'AvaliableElevator = %s,Index = %d' % (AvaliableElevator,Len.index(min(Len)))
		try:
			#print 'Find Idle %s GetElevator %s' % (customer,AvaliableElevator[Len.index(min(Len))])
			return AvaliableElevator[Distance.index(min(Distance))]
		except:
			pass


		# 不存在空闲电梯，查找最优路线电梯
		if customer.NowFloor < customer.DestFloor:
			custDirection = 'Up'
		else:
			custDirection = 'Down'

		for elevator in AvaliableElevator:
			if elevator.Direction == custDirection:
				# 两者方向一致，且经过
				if custDirection == 'Up' and customer.NowFloor > elevator.NowFloor:
					return elevator
				if custDirection == 'Down' and customer.NowFloor < elevator.NowFloor:
					return elevator
		return None
	
		assert False

	def GetAllStatus(self):
		''' 获得所有Elevator的当前状态 '''
		pass
	
if __name__ == '__main__':
	eleCtl = ElevatorControl(10,1,2)
