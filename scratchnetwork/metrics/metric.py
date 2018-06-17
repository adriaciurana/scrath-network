from ..losses.loss import Loss
import numpy as np
class Metric(Loss):
	def __init__(self, node, params={}):
		params['compute_backward'] = False	
		# No produce dependencias ya que no participa en el forward (porque es un nodo final) ni participa en el backward porque es una metrica.
		super(Metric, self).__init__(node, params=params)


	def forward(self, inputs):
		super(Metric, self).forward(inputs)

		
