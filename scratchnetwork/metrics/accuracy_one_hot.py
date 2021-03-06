from .metric import Metric
import numpy as np
class AccuracyOneHot(Metric):
	def __init__(self, node, params=None):
		if params is None:
			params = {}
			
		super(AccuracyOneHot, self).__init__(node, params=params)


	def forward(self, inputs):
		super(AccuracyOneHot, self).forward(inputs)

		pred, true = inputs
		pred = np.argmax(pred, axis=-1)
		true = np.argmax(true, axis=-1)

		return np.sum(pred == true) / pred.shape[0]
