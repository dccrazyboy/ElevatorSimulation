#!/usr/bin/env python
#coding: utf-8
'''
@author: DC
@license: 
@contact: dc.china@qq.com
@see: 

'''

class FloorView(object):
	""" 楼层显示类，用于处理楼层信息显示
		
		@ivar FloorInfo: 楼层信息列表
			
			存储内容为：
			
			{'WaitingCustomer' : [], 'InRequestCustomer' : []}
		@type FloorInfo: dict
	
	"""
	def __init__(self):
		''' 初始化 '''
		self.FloorInfo = []

		for i in range(0,41):
			self.FloorInfo.append({'WaitingCustomer' : [], 'InRequestCustomer' : []})
		# 初始化日志
		#print self.FloorInfo
		
		#self.logger = Logger()

	def __str__(self):
		''' 打印所有楼层信息 '''
		printStr = '[FloorView] \n'
		for floorNum in range(1,41):
			printStr = printStr + '%d : WaitingCustomer: %d,InRequestCustomer: %d\n' % \
					   (floorNum,len(self.FloorInfo[floorNum]['WaitingCustomer']),\
						len(self.FloorInfo[floorNum]['InRequestCustomer']))
		return printStr

	def UpDateFloorView(self,CustomerList):
		''' 更新Floor视图 
			@type CustomerList: list
			@param CustomerList: 所有顾客信息
		
		'''
		# 清空原视图
		self.FloorInfo = []

		for i in range(0,41):
			self.FloorInfo.append({'WaitingCustomer' : [], 'InRequestCustomer' : []})
			
		for cust in CustomerList:
			if cust.Status == 'Waiting':
				self.FloorInfo[cust.NowFloor]['WaitingCustomer'].append(cust)
			elif cust.Status == 'InRequest':
				self.FloorInfo[cust.NowFloor]['InRequestCustomer'].append(cust)
			else:
				pass

	def GetFloorInfo(self,FloorNum):
		''' 获得楼层信息 
			@type FloorNum: int
			@param FloorNum: 查询楼层
		
			@rtype: tuple
			@return: 当前楼层顾客信息
		'''
		return (self.FloorInfo[FloorNum]['WaitingCustomer'],self.FloorInfo[FloorNum]['InRequestCustomer'])

	
if __name__ == '__main__':
	f = FloorView()
