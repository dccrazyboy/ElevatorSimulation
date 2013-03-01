#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 

'''
from Customer import Customer
import random

class CustomerControl(object):
	""" 顾客控制类，控制所有顾客行为 
		
		@ivar AllCustomer: 所有客户列表
		@type AllCustomer: Customer
		
		@ivar ArrivalTable: 客户到达顺序列表
		@type ArrivalTable: dict
		
		@ivar LastArrivalTime: 最后一位客户到达时间

			用于优化，如果这个时间没变，则不更新
		@type LastArrivalTime: int
		
		@ivar AllInRequestTime: 所有客户等待时间
		@type AllInRequestTime: Customer
	"""
	def __init__(self,CustomerNum,SimulateTime):
		''' 初始化 
			@type CustomerNum: int
			@param CustomerNum: 总顾客数
		
			@type SimulateTime: int
			@param SimulateTime: 模拟时间
		
		'''
		self.AllCustomer = []
		self.ArrivalTable = {}
		self.LastArrivalTime = 0

		# 用户离开时统计等待时间
		self.AllInRequestTime = {}

		# 初始化日志
		#self.logger = Logger()
		
		# 随机初始化ArrivalTable
		for i in range(1,SimulateTime+1):
			self.ArrivalTable[i] = []
		for i in range(1,CustomerNum+1):
			ArrivalTime = random.choice(range(1,SimulateTime+1))
			self.ArrivalTable[ArrivalTime].append(i)
			if ArrivalTime > self.LastArrivalTime:
				self.LastArrivalTime = ArrivalTime
		#self.logger.debug('CustomerControl::__init__ ArrivalTable = %s' % self.ArrivalTable)

		#print 'ArrivalTable:'
		#for key,value in self.ArrivalTable.items():
		#	 if value != []:
		#		 print '%d: %s' % (key,value)

	def __str__(self):
		''' 打印所有顾客状态 '''
		printStr = '[CustomerControl] \n'
		#for cust in self.AllCustomer:
		#	 printStr = printStr + str(cust) + '\n'
		printStr = printStr + 'self.AllCustomer = %d' % len(self.AllCustomer)
		return printStr
	
	def AddTimer(self,NowTime):
		''' 调用此函数通知时间加1，更新内部状态
			@type NowTime: int
			@param NowTime: 当前时间，一般不做使用
		'''
		# 删除离开状态的Customer
		for customer in self.AllCustomer:
			if customer.Status == 'Exiting':
				self.AllInRequestTime[customer.ID] = customer.InRequestTime
				self.AllCustomer.remove(customer)
				del customer
				
		# 检查所有顾客是否都调度完成
		if NowTime > self.LastArrivalTime and len(self.AllCustomer) == 0:
			# 调度完成
			return 'Finish'
		
		# 产生新的Customer
		if NowTime <= max(self.ArrivalTable.keys()):
			for CustomerID in self.ArrivalTable[NowTime]:
				newCustomer = Customer(CustomerID,random.choice(range(1,11)))
				self.AllCustomer.append(newCustomer)
				#self.IdleCustomer.append(newCustomer)
				
		# 通知所有Customer的Timer加1
		for customer in self.AllCustomer:
			customer.AddTimer(NowTime)


	def GetIdleCustomer(self):
		''' 获得当前空闲用户 
			@rtype: Customer
			@return: 空闲顾客
		'''
		IdleCustomer = []
		for customer in self.AllCustomer:
			if customer.Status == 'Idle':
				IdleCustomer.append(customer)
		return IdleCustomer
	
	def GetAllCustomer(self):
		''' 获得所有Customer 
			@rtype: list
			@return: 所有客户列表
		'''
		return self.AllCustomer
	
	def GetAllInRequestTime(self):
		''' 获得AllInRequestTime 
			@rtype: list
			@return:所有顾客请求等待时间
		'''
		return self.AllInRequestTime
	
if __name__ == '__main__':
	custCtl = CustomerControl(1,5)
	custCtl.AddTimer(1)
	custCtl.AddTimer(2)
	custCtl.AddTimer(3)
	custCtl.AddTimer(4)
	custCtl.AddTimer(5)
