#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 
'''

class Elevator(object):
	''' 电梯类，每一个电梯一个对象
		
		@ivar Tag: 电梯标号
		@type Tag: str
		
		@ivar AvaliableFloor: 可到达楼层
		@type AvaliableFloor: list
		
		@ivar MaxCustomer: 最大乘员数
		@type MaxCustomer: int
		
		@ivar NowFloor: 当前楼层
		@type NowFloor: int
		
		@ivar CustomerList: 电梯内客户列表 
		@type CustomerList: list
		
		@ivar RequsetList: 请求客户列表
		@type RequsetList: list
		
		@ivar Direction: 运行方向'Up' or 'Down'
		@type Direction: str
		
		@ivar TrackLow: 需要达到最低楼层
		@type TrackLow: int
		
		@ivar TrackHigh: 需要到达最高楼层
		@type TrackHigh: int
		
		@ivar Status: 当前电梯状态

			- 'Idle':
				Elevator处于空闲状态，等待请求。控制权为控制类。
			- 'Running':
				Elevator处于运行状态。控制权为自己。	
			- 'Boarding':
				Elevator有顾客正在进入电梯。控制权为控制类。
			- 'Landing':
				Elevator有顾客正在离开电梯。控制权为控制类。
		@type Status: str
		
		@ivar TimeRemain: 表示某状态需要等待的时间

			只在Status为'Running'、'Boarding'、'Landing'时有效
		@type TimeRemain: int
		
		@ivar Speed: 电梯运行速度,层/秒
		@type Speed: int
		
		@ivar BoardTime: 上下电梯时间
		@type BoardTime: int
		
		@ivar IdleTime: 电梯空闲时间
		@type IdleTime: int
		
		@ivar RunningTime: 电梯运行时间
		@type RunningTime: int
	'''
	def __init__(self,Tag,AvaliableFloor,MaxCustomer,InitFloor,Speed,BoardTime):
		''' 初始化电梯信息 
			@type Tag: str
			@param Tag: 电梯标号

			@type AvaliableFloor: list
			@param AvaliableFloor: 可到达楼层

			@type MaxCustomer: int
			@param MaxCustomer: 最大乘员量

			@type InitFloor: int
			@param InitFloor: 电梯初始楼层

			@type Speed: int
			@param Speed: 电梯运行速度 
						Speed秒/层

			@type BoardTime: int
			@param BoardTime: 顾客上下电梯耗时
		'''
		self.Tag = Tag
		self.AvaliableFloor = AvaliableFloor
		self.MaxCustomer = MaxCustomer
		self.NowFloor = InitFloor
		self.CustomerList = []		# 存储电梯内的顾客
		self.RequsetList = []		# 存储被分配到这个电梯而未上电梯的顾客
		self.Direction = 'Up'		# 当前电梯运行方向，'Up'、'Down'
		self.TrackLow = 1			# 电梯需要到达的最小最大楼层
		self.TrackHigh = 1
		
		self.Status = 'Idle'
		self.TimeRemain = 0
		self.Speed = Speed
		self.BoardTime = BoardTime

		# 统计时间
		self.IdleTime = 0
		self.RunningTime = 0
		
		# 初始化日志
		#self.logger = Logger()

		#self.logger.debug('[Elevator::__init__] Tag = %s ,InitFloor = %s' % (Tag,InitFloor))
		pass

	def __str__(self):
		''' 打印电梯信息 '''
		CustomerDestFloor = []
		for cust in self.CustomerList:
			CustomerDestFloor.append([cust.ID,cust.DestFloor])
		RequestNowFloor = []
		for cust in self.RequsetList:
			RequestNowFloor.append([cust.ID,cust.NowFloor])
			
		printStr = '[Elevator] Tag = %s, NowFloor = %d,Status = %s CustomerDest = %s, RequsetNow = %s' % \
			(self.Tag,self.NowFloor,self.Status,CustomerDestFloor,RequestNowFloor)
		
		return printStr
	
	def AddTimer(self,NowTime):
		''' 调用此函数通知时间加1，更新内部状态
			@type NowTime: int
			@param NowTime: 当前时间，一般不做使用
		'''
		try:
			#print self
			if self.Status == 'Idle':
				# 电梯空闲，无请求
				# 不作处理，由控制类改变此状态
				self.IdleTime = self.IdleTime + 1
				return
			
			if self.Status == 'Running':
				self.RunningTime = self.RunningTime + 1
				# 电梯正在正常运行
				self.TimeRemain = self.TimeRemain - 1
				#print 'TimeRemain = %d' % self.TimeRemain
				assert self.TimeRemain >= 0
				if self.TimeRemain == 0:
					# 到达新的楼层
					self.NowFloor = self.NowFloor + self.__GetFloorOffset()
					#print '%s arrive at %d' % (self,self.NowFloor)
					#self.TimeRemain = self.Speed

					for Cust in self.CustomerList:
						if Cust.DestFloor == self.NowFloor:
							# 到达顾客请求楼层，通知顾客退出电梯
							Cust.LandingNotify(self)
							self.CustomerList.remove(Cust)
							self.__UpdateTrack()
							# 等待顾客退出电梯
							self.Status = 'Landing'
							self.TimeRemain = self.BoardTime
							return
						
					# 查询请求列表里的顾客
					for Cust in self.RequsetList:
						if Cust.NowFloor == self.NowFloor:
							# 从请求列表中删除
							self.RequsetList.remove(Cust)
							# 让顾客进入电梯
							Cust.BoardingNotify(self)
							self.CustomerList.append(Cust)
							self.__UpdateTrack()
							# 等待顾客进入电梯
							self.Status = 'Boarding'
							self.TimeRemain = self.BoardTime
							return
					self.TimeRemain = self.Speed
				return

			if self.Status == 'Landing':
				self.RunningTime = self.RunningTime + 1
				# 电梯正在等待顾客退出电梯
				self.TimeRemain = self.TimeRemain - 1
				if self.TimeRemain == 0:
					# 完成退出电梯
					# 遍历剩余顾客，看是否需要退出电梯
					for Cust in self.CustomerList:
						if Cust.DestFloor == self.NowFloor:
							# 到达顾客请求楼层，通知顾客退出电梯
							Cust.LandingNotify(self)
							self.CustomerList.remove(Cust)
							self.__UpdateTrack()
							# 等待顾客退出电梯
							self.Status = 'Landing'
							self.TimeRemain = self.BoardTime
							return
					# 检测电梯中是否还有人
					if self.CustomerList == []:
						# 若顾客列表中没有顾客了
						# 检测请求队列中是否还有顾客
						if self.RequsetList == []:
							# 均没有顾客
							self.Status = 'Idle'
						else:
							# 请求列表中有顾客
							self.Status = 'Running'
							self.TimeRemain = self.Speed
					else:
						# 还存在顾客，返回Running状态
						self.Status = 'Running'
						self.TimeRemain = self.Speed
				return
			
			if self.Status == 'Boarding':
				self.RunningTime = self.RunningTime + 1
				# 电梯正在等待顾客进入电梯
				self.TimeRemain = self.TimeRemain - 1
				if self.TimeRemain == 0:
					# 完成进入电梯
					# 查询请求列表里的顾客
					for Cust in self.RequsetList:
						if Cust.NowFloor == self.NowFloor:
							# 从请求列表中删除
							self.RequsetList.remove(Cust)
							# 让顾客进入电梯
							Cust.BoardingNotify(self)
							self.CustomerList.append(Cust)
							self.__UpdateTrack()
							#assert len(self.CustomerList) <= self.MaxCustomer
							# 等待顾客进入电梯
							self.Status = 'Boarding'
							self.TimeRemain = self.BoardTime
							return
					# 重新调度
					self.Status = 'Running'
					self.TimeRemain = self.Speed
				return
		finally:
			pass
			
		# self.Status 不在状态表中
		assert False
		
	def RunningNotify(self,customer):
		''' 接受顾客进入请求 
			@type customer: Customer
			@param customer: 请求进入的顾客
		
		'''
		# 将客户加入列表中
		self.RequsetList.append(customer)
		if self.Status == 'Idle':
			# 当前状态为空闲
			self.Status = 'Running'
			self.TimeRemain = self.Speed
		#print '%s RunningNotify %s' % (self,customer)

	def GetNowStatus(self):
		''' 获得当前运行状态 
			
			@rtype: tuple
			@return: 当前状态,(Tag,Status,NowFloor,CustomerList,RequsetList,IdleTime,RunningTime)
		
		'''
		return (self.Tag,self.Status,self.NowFloor,self.CustomerList,self.RequsetList,self.IdleTime,self.RunningTime)

	def __UpdateTrack(self):
		''' 更新TrackHigh和TrackLow的值 '''
		# 所有的客户列表的楼层都需要满足
		DestList = []
		for customer in self.CustomerList:
			DestList.append(customer.DestFloor)
		for request in self.RequsetList:
			DestList.append(request.NowFloor)
		if DestList == []:
			return
		self.TrackLow = min(DestList)
		self.TrackHigh = max(DestList)
		
	def __GetFloorOffset(self):
		''' 获得下一层的偏移量 
			
			@rtype: int
			@return: 下一层的偏移1 or -1
		'''
		if self.CustomerList == []:
			NextFloor = self.RequsetList[0].NowFloor
		else:
			NextFloor = self.CustomerList[0].DestFloor

		if self.NowFloor > NextFloor:
			self.Direction = 'Down'
			return -1
		elif self.NowFloor < NextFloor:
			self.Direction = 'Up'
			return 1
		else:
			return 0
		
		
if __name__ == '__main__':
	pass
