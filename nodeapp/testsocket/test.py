# -*-coding:utf-8-*-
import random as rd
import time

def main():
	def logging_tool(func):
		def wrapper(*arg, **kwargs):
			print('%s is running...' % func.__name__)
			func()  # 把today当作参数传递进来，执行func()就相当于执行today()
		return wrapper

	@logging_tool
	def today():
		print('2018-05-25')

	# today = logging_tool(today)  # 因为装饰器logging_tool(today)返回函数对象wrapper，故这条语句相当于today=wrapper
	today()  # 执行today() 就相当于执行wrapper()
if __name__ == '__main__':
	main()


