class Layer(object):
	def __init__(self, node, params={}):
		self.node = node
		# pesos de la capa
		self.weights = Layer.Weights()
		# valores intermedios de la capa
		self.values = Layer.Values()
		# parametros de la capa
		self.params = params

		# regularizacion
		self.regularization = lambda weight: 0
		self.is_trainable = True
			



	def computeSize(self):
		if 'same_input_shape' in self.params:
			if self.in_size[:1] == self.in_size[:-1]:
				raise Network.DifferentInputShape("El tipo de datos en la capa " \
					 + self.node.name + " debe ser igual en todos los casos. "+str(self.in_size))

	def compile(self):
		# inicializaciones
		if 'compute_forward_in_prediction' in self.params:
			self.node.compute_forward_in_prediction = self.params['compute_forward_in_prediction']

		if 'compute_backward' in self.params:
			self.node.compute_backward = self.params['compute_backward']

		if 'number_of_inputs' in self.params:
			if self.params['number_of_inputs'] < len(self.node.prevs):
				raise Network.NumberInputsException("Numero de entradas excedidas (" \
				 + self.params['number_of_inputs'] + ") en " + type(self).__name__ + ":" + self.node.name)
			
			elif self.params['number_of_inputs'] > len(self.node.prevs):
				raise Network.NumberInputsException("Numero de entradas inferiores (" \
				 + self.params['number_of_inputs'] + ") en " + type(self).__name__ + ":" + self.node.name)
		
		if 'regularization' in self.params:
			self.regularization = self.params['regularization'].function

	def firstForward(self, inputs):
		pass

	def forward(self, inputs):
		pass
	
	def backward(self, doutput=None):
		raise NotImplemented
	"""
		WEIGHTS:
	"""
	class Weights(object):
		def copy(self):
			c = self.__class__
			copy_weights_instance = c.__new__(c)
			
			for w in self.__attrs__:
				setattr(copy_weights_instance, w, copy.copy(getattr(self, w)))
			return copy_weights_instance

	class Values(object):
		def copy(self):
			c = self.__class__
			copy_values_instance = c.__new__(c)
			
			for v in self.__attrs__:
				setattr(copy_values_instance, v, copy.copy(getattr(self, v)))
			return copy_values_instance

	def getRegularization(self, name, weight):
		if isinstance(self.regularization, dict):
			return self.regularization[name](weight)
		else:
			return self.regularization(weight)
	""" 
	Para actualizar un peso se necesitan diversos parametros:
		Loss: donde se esta contribuyendo, desconocemos el funcional que se ha usado 
			para unir los batches (Normalmente es la media). Pero es importante saber que cada loss es acumulada de forma independiente.
		weights_losses: Indica el peso de cada loss, por defecto este es 1/num_losses
		name: indica el nombre del parametro a actualizar
	"""
	def correctWeight(self, name, dweight):
		# primero obtenemos el peso a corregir
		w = getattr(self.weights, name)
		# aplicamos el funcional respecto al batch
		dweight /= self.node.network.batch_size
		# añadimos la regularizacion
		# actualizamos la derivada
		dweight = dweight + self.getRegularization(name, w)

		# realizamos la correccion con respecto al optimizador
		setattr(self.weights, name, w + self.node.network.optimizer.step(dweight))

	def copy(self, node):
		c = self.__class__
		copy_layer_instance = c.__new__(c)
		copy_layer_instance.node = node
		copy_layer_instance.weights = self.weights.copy()
		copy_layer_instance.values = self.values.copy()
		return copy_layer_instance