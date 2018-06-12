import sys
import os
import numpy as np

sys.path.append(os.path.dirname(__file__)+"../")
from network import Network
from network.layers import Input
from network.layers import FC
from network.layers import ReLU
from network.losses import Loss
from network.metrics import Metric
net = Network()
inputX = net.Node("Input", Input, [10])
inputY = net.Node("Y", Input, [1])

B = net.Node("B", FC, 10)
Br = net.Node("B_relu", ReLU)
C = net.Node("Output", FC, 1)

L1 = net.Node("Loss", Loss)
M1 = net.Node("Metric", Metric)

inputX.addNext(B)
B.addNext(Br)
Br.addNext(C)

L1.addPrev(C)
L1.addPrev(inputY)

M1.addPrev(C)
M1.addPrev(inputY)

net.compile(losses=[L1], metrics=[M1])
net.start(inputs=[inputX], outputs=[C])
net.plot("example_1.png")

# Llenamos
a = 2*(np.random.rand(1000, 10) - 0.5)
b = np.dot(a, np.random.rand(10, 1)) #np.dot(np.sign(a)*a**2, 100*np.random.rand(10, 1))

batch_index = 0
batch_size = 20
for i in range(100000):
	Xaux = a[batch_index:(batch_index + batch_size)]
	Yaux = b[batch_index:(batch_index + batch_size)]

	net.train_batch({'Input': Xaux}, {'Y': Yaux})

	batch_index += batch_size
	if batch_index >= a.shape[0]:
		batch_index = 0
	if i % 500 == 0:
		net.monitoring()
out = net.predict({'Input': a})
print(np.hstack((out['Output'], b)))