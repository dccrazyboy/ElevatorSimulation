#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 

'''
from Timer import Timer
from ElevatorControl import ElevatorControl
from CustomerControl import CustomerControl
from FloorView import FloorView
import time

class ElevatorSimulation(object):
	''' 电梯模拟类 
		
		@ivar IsAuto: 是否是自动模式
			
			自动模式下时间每隔1S加1，手动模式需手动调用AddTimer使时间加1
		@type IsAuto: bool
		
		@ivar timer: 时间控制类
		@type timer: Timer
		
		@ivar elevatorCtl: 电梯控制类
		@type elevatorCtl: ElevatorControl
		
		@ivar customerCtl: 顾客控制类
		@type customerCtl: CustomerControl
		
		@ivar floorView: 楼层显示类
		@type floorView: FloorView
	'''
	def __init__(self,K,N,M,S,T,AutoSimu):
		''' 初始化
			@type K: int
			@param K: 每部电梯的最大乘员量 [10,18]
			
			@type N: int
			@param N:  顾客总人数 (0,1000)

			@type M: int
			@param M: 顾客到达总时间 (0,10)

			@type S: int
			@param S: 电梯运行速度 [1,5]
			
			@type T: int
			@param T: 每人上下时间 [2,10]
			
			@type AutoSimu: bool 
			@param AutoSimu: 是否是自动模式 

'''
		# 初始化日志
		#self.logger = Logger()

		# 检查传入参数
		assert K in range(10,19)
		assert N in range(1,1000)
		assert M in range(1,10)
		assert S in range(1,6)
		assert T in range(2,11)
		
		# 开始电梯模拟
		#self.logger.debug('===================================================================')
		#self.logger.debug('[ElevatorSimulation::__init__] Start New ElevatorSimulation!')
		print '[ElevatorSimulation::AddTimer] Start New ElevatorSimulation!'
		print '==================================================================='
		# 用于控制是否自动模拟，若为False则需要手动调用AddTimer
		self.IsAuto = AutoSimu
		
		self.timer = Timer()
		# 创建三个对象，用于总控制
		self.elevatorCtl = ElevatorControl(MaxCustomer = K, Speed = S, BoardTime = T)
		self.customerCtl = CustomerControl(CustomerNum = N, SimulateTime = M * 60)
		self.floorView = FloorView()

		# 将两个控制对象注册到Timer
		self.timer.RegisterObject(self.elevatorCtl)
		self.timer.RegisterObject(self.customerCtl)

		if self.IsAuto:
			while (1):
				ret = self.AddTimer()
				if ret == 'Finish':
					#self.logger.info('[ElevatorSimulation::AddTimer] ElevatorSimulation Finish!')
					#self.logger.debug('===================================================================')
					print '[ElevatorSimulation::AddTimer] ElevatorSimulation Finish!'
					print '==================================================================='
					break
				#time.sleep(1)
				
	def AddTimer(self):
		''' 调用此函数通知时间加1，更新内部状态
		'''

		
		# 对空闲人员进行分配
		IdleCustomer = self.customerCtl.GetIdleCustomer()
		for customer in IdleCustomer:
			elevator = self.elevatorCtl.GetBestElevator(customer)
			if elevator != None:
				elevator.RunningNotify(customer)
				customer.InRequestNotify(elevator)

		# 更新楼层显示类
		self.floorView.UpDateFloorView(self.customerCtl.GetAllCustomer())
		
		#print self.floorView
		
		# 通知其他对象时间加1
		return self.timer.AddTimer()



if __name__ == '__main__':
	#simu = ElevatorSimulation(10,999,9,5,10,True)
	#simu = ElevatorSimulation(10,10,1,1,2,True)

	# profile test
	#import profile
	#profile.run("ElevatorSimulation(10,999,9,5,10,True)", "prof.txt")
	#import pstats
	#p = pstats.Stats("prof.txt")
	
	# cProfile test
	import cProfile
	cProfile.run("ElevatorSimulation(10,100,1,1,2,True)", "result")
	import pstats
	p = pstats.Stats("result")
	p.sort_stats("time").print_stats()
