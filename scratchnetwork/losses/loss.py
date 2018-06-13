from ..layers.layer import Layer
import numpy as np
class Loss(Layer):
	def __init__(self, node, params= {}):
		params['same_input_shape'] = True
		params['compute_forward_in_prediction'] = False
		super(Loss, self).__init__(node, params)

	def computeSize(self):
		return tuple([1])
		
	def forward(self, inputs):
		super(Loss, self).forward(inputs)

	def derivatives(self, doutput=None):
		pass