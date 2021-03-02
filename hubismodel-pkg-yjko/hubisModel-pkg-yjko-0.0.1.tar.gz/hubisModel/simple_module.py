import cv2
import matplotlib.pyplot as plt
import numpy
import tensorflow as tf


class MyClass:
	model = 0

	def __init__(self):
		self.model = numpy.random.rand(2, 2) * 100
		print
		"MyClass instantiated"
		print
		self.model

	def __del__(self):
		print
		"MyClass deleted"

	def Sum(self):
		return numpy.sum(self.model)

	def Avr(self, count):
		return numpy.sum(self.model) / count
	def Cosine(self):
		return numpy.cos(numpy.sum(self.model))


def simple_func(a, b):
	plt.plot([1, 2, 3, 4])
	plt.ylabel('y-label')
	plt.show()
	#print("a:, a)
	#print("b:, b)
	print("python func called")
	c = a+b
	return numpy.cos(c)




