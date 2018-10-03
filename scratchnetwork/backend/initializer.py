import numpy as np
class Initializer(object):
	def __init__(self, name, *args):
		self.name = name
		self.args = args

	def get(self, shape):
		if self.name == 'ones':
			return np.ones(shape=shape)
		
		elif self.name == 'zeros':
			return np.zeros(shape=shape)
		
		elif self.name == 'constant':
			return np.ones(shape=shape)*self.args[0]
		
		elif self.name == 'rand':
			# 0-1 uniform
			if len(self.args) == 0:
				return np.rand(*shape)
			
			# 0-N
			elif len(self.args) == 1:
				return np.rand(*shape)*self.args[0]

			# a-b
			elif len(self.args) == 2:
				return self.args[0] + np.random.rand(*shape)*(self.args[1] - self.args[0])

		elif self.name == 'normal':
			if len(self.args) == 0:
				return np.random.randn(*shape)

			elif len(self.args) == 2:
				return np.random.randn(*shape)*self.args[1] + self.args[0]

		elif self.name == 'xavier':
			return np.rand(*shape) * np.sqrt(2.0/shape[1])

		elif self.name == 'lecun':
			fan_in = np.prod(shape)
			stddev = np.sqrt(1./fan_in)
			return np.random.normal(loc = 0, scale=stddev, size=shape)