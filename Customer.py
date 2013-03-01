#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 

'''
import random

class Customer(object):
	""" 顾客类，每一个顾客一个对象 
	
		@ivar ID: 顾客编号
		@type ID: int 
	
		@ivar LaunchNum: 乘坐电梯次数
		@type LaunchNum: int 
	
		@ivar NowFloor: 当前楼层
		@type NowFloor: int
	
		@ivar DestFloor: 目标楼层
		@type DestFloor: int
	
		@ivar Status: 当前状态

			Status域存储当前的状态，分别为：
				- 'Idle':
					Customer处于空闲状态，等待电梯。控制权为控制类。
				- 'Waiting':
					Customer处于随机停留状态。控制权为自身。
				- 'InRequest':
					Customer已确定乘坐电梯，等待电梯到来。控制权为自身。
				- 'InElevator':
					Customer处于电梯内。控制权为自身。
				- 'Boarding':
					Customer正在进入电梯。控制权为控制类。
				- 'Landing':
					Customer正在离开电梯。控制权为控制类。
				- 'Exiting':
					Customer正在进入电梯。控制权为控制类。
		@type Status: str
	
		@ivar TimeRemain: 某状态剩余时间

			只在Status为'Waiting'、'Boarding'、'Landing'时有效
		@type TimeRemain: int
	
		@ivar Elevator: 关联的电梯

			只在Status为'InElevator'、'Boarding'、'Landing'时有效
		@type Elevator: Elevator
	
		@ivar InRequestTime: 统计等待时间
		@type InRequestTime: int
		
	"""
	def __init__(self,ID,LaunchNum):
		''' 初始化 
			@type ID: int
			@param ID: 顾客编号
		
			@type LaunchNum: int
			@param LaunchNum: 乘坐电梯次数
		'''
		self.ID = ID
		self.LaunchNum = LaunchNum
		self.NowFloor = 1
		self.DestFloor = random.randint(2,40)
		self.Status = 'Idle'
		self.TimeRemain = 0
		self.Elevator = None

		self.InRequestTime = 0
		
		# 初始化日志
		#self.logger = Logger()
		
		#self.logger.debug('[Customer::__init__] ID = %d,LaunchNum = %d' % (self.ID,self.LaunchNum))
		
	def __str__(self):
		''' 打印顾客信息 '''
		try:
			ElevatorTag = self.Elevator.Tag
		except:
			ElevatorTag = self.Elevator
		printStr = '[Customer] ID = %d,Status = %s,NowFloor = %d,DestFloor = %d,LaunchNum = %d,ElevatorTag = %s' % \
				   (self.ID,self.Status,\
					self.NowFloor,self.DestFloor,self.LaunchNum,ElevatorTag)
		return printStr

	def AddTimer(self,NowTime):
		''' 调用此函数通知时间加1，更新内部状态
			@type NowTime: int
			@param NowTime: 当前时间，一般不做使用
		'''
		try:
			#print self
			# 进行状态转移
			if self.Status == 'Idle':
				# 等待控制类调度，自身不做任何处理
				return
			
			if self.Status == 'Waiting':
				# 当前状态为Waiting，进行判断
				self.TimeRemain = self.TimeRemain - 1
				if self.TimeRemain == 0:
					if self.LaunchNum > 0:
						# 请求下一次电梯
						self.Status = 'Idle'
						self.DestFloor = random.choice(range(1,self.NowFloor) + range(self.NowFloor + 1,41))
						return
					elif self.LaunchNum == 0:
						# 顾客完成所有乘坐，回到1楼
						self.Status = 'Idle'
						self.DestFloor = 1
						return
					else:
						assert False
				return

			if self.Status == 'InRequest':
				# 当前状态在Elevator等待队列中，由控制类控制上电梯
				self.InRequestTime = self.InRequestTime + 1
				return
			
			if self.Status == 'InElevator':
				# 当前状态在Elevator中，由控制类控制下电梯
				return
			
			if self.Status == 'Boarding':
				# 正在进入电梯，等待
				self.TimeRemain = self.TimeRemain - 1
				if self.TimeRemain == 0:
					# 进入电梯完毕
					self.Status = 'InElevator'
				return

			if self.Status == 'Landing':
				# 退出电梯
				self.TimeRemain = self.TimeRemain - 1
				if self.TimeRemain == 0:
					# 退出电梯完毕
					self.Elevator = None
					self.LaunchNum = self.LaunchNum - 1
					assert self.TimeRemain >= 0
					# 刚下电梯，判断乘坐是否结束
					if self.LaunchNum < 0:
						# 乘坐结束，此乘客退出
						assert self.NowFloor == 1
						self.Status = 'Exiting'
						return
					else:
						# 还需要乘坐，随机停留
						self.Status = 'Waiting'
						self.TimeRemain = random.randint(10,120)
						return
				return

			if self.Status == 'Exiting':
				# 等待控制类调度，自身不做任何处理
				return
			
		finally:
			pass
			
		# self.Status不在状态表中
		assert False

	def InRequestNotify(self,elevator):
		''' 请求电梯时此函数被调用 
			@type elevator: Elevator
			@param elevator: 请求的电梯
		
		'''
		# 当 self.Status == 'Idle'时才能调用
		assert self.Status == 'Idle'
		self.Status = 'InRequest'
		# 此时等待Elevator
		self.Elevator = elevator
		#print '%s InRequestNotify %s' % (self,elevator)

	def BoardingNotify(self,elevator):
		''' 进入电梯时此函数被调用 
			@type elevator: Elevator
			@param elevator: 将进入的电梯
		
		'''
		# 当 self.Status == 'InRequest'时才能调用
		assert self.Status == 'InRequest'
		self.Status = 'Boarding'
		# 此时的时间控制和Elevator相同
		self.TimeRemain = elevator.BoardTime
		self.Elevator = elevator
		#print '%s BoardingNotify %s' % (self,elevator)
		
		
	def InElevatorNotify(self,elevator):
		''' 进入电梯后，电梯处于运行状态此函数被调用 
			@type elevator: Elevator
			@param elevator: 关联电梯
		
		'''
		# 当 self.Status == 'Boarding' or 'InElevator'时才能调用
		assert self.Status == 'Boarding' or 'InElevator'
		self.Status = 'InElevator'
		# 当前位置和电梯相同
		self.NowFloor = elevator.NowFloor
		self.Elevator = elevator
		#print '%s InElevatorNotify %s' % (self,elevator)

	def LandingNotify(self,elevator):
		''' 离开电梯此函数被调用 
			@type elevator: Elevator
			@param elevator: 将离开的电梯
		
		'''
		# 当 self.Status == 'InElevator'时才能调用
		# 确认到达请求楼层
		assert self.Status == 'InElevator'
		# 因为存在电梯时间先加1，人时间后加1的问题，所以这里人的楼层不可能等于电梯的楼层。
		self.NowFloor = elevator.NowFloor
		
		self.Status = 'Landing'
		# 此时的时间控制和Elevator相同
		self.TimeRemain = elevator.BoardTime
		self.Elevator = elevator
		#print '%s LandingNotify %s' % (self,elevator)

	def GetNowStatus(self):
		''' 获得当前顾客状态 
			
			@rtype: tuple
			@return: 当前状态,(ID,Status,NowFloor,DestFloor,LaunchNum,InRequestTime)
		
		'''
		return (self.ID,self.Status,self.NowFloor,self.DestFloor,self.LaunchNum,self.InRequestTime)
	
if __name__ == '__main__':
	from Elevator import Elevator
	eve = Elevator('E0',range(1,41),10,InitFloor = 1,Speed = 2,BoardTime = 2)
	cust = Customer(1,5)
	cust.AddTimer(1)
	cust.AddTimer(2)
	cust.AddTimer(3)
