#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 

'''

class Timer(object):
	""" 时间控制类，用于通知其他对象时间加1 
		
		@ivar NowTime: 当前时间
		@type NowTime: int
		
		@ivar RegObj: 注册的对象
		@type RegObj: object
	"""
	def __init__(self):
		''' 初始化 '''
		self.NowTime = 0 # 当前运行时间
		self.RegObj = [] # 注册的所有需要被通知对象

		# 初始化日志
		#self.logger = Logger()

	def __str__(self):
		''' 打印当前时间信息 '''
		printStr = '[Timer] NowTime = %d' % (self.NowTime)
		return printStr
	
	def RegisterObject(self,obj):
		''' 注册对象obj到Timer类中，以后将会被通知 
			@type obj: object
			@param obj: 拥有Addtime方法的任意对象
		
		'''
		self.RegObj.append(obj)
		#self.logger.debug('[Timer::RegisterObject] obj = %s' % obj)
	
	def CancelObject(self,obj):
		''' 取消对象obj的注册 
			@type obj: object
			@param obj: 之前注册的对象
		'''
		self.RegObj.remove(obj)
		#self.logger.debug('[Timer::CancelObject] obj = %s' % obj)
		
	def AddTimer(self):
		''' 调用此函数使Timer计数加1 '''
		#print ''
		#print self
		self.NowTime = self.NowTime + 1
		for obj in self.RegObj:
			#print obj
			ret = obj.AddTimer(self.NowTime)
			if ret == 'Finish':
				print 'LastTime = %d' % self.NowTime
				return 'Finish'
	def GetNowTime(self):
		''' 获取当前时间 '''
		return self.NowTime

	
if __name__ == '__main__':
	t = Timer()
	print t
