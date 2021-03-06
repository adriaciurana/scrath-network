import sys, os
import numpy as np
sys.path.append(os.path.dirname(__file__)+"../../../")
from scratchnetwork import Network
from scratchnetwork.layers import Input, FC, ReLU
from scratchnetwork.losses import MSE
from scratchnetwork.metrics import MRSE
from scratchnetwork.optimizers import SGD

net = Network()
inputX = net.Node(Input, "Input", [10])
inputY = net.Node(Input, "Y", [1])

B = net.Node(FC, "B", 10)
Br = net.Node(ReLU, "B_relu")
C = net.Node(FC, "Output", 1)

L1 = net.Node(MSE, "MSE")
M1 = net.Node(MRSE, "MRSE")

inputX.addNext(B)
B.addNext(Br)
Br.addNext(C)

L1.addPrev(C)
L1.addPrev(inputY)

M1.addPrev(C)
M1.addPrev(inputY)

net.compile(inputs=[inputX], outputs=[C], losses=[L1], metrics=[M1], optimizer=SGD(lr=0.1, clip_norm=10))
net.plot(os.path.basename(sys.argv[0]).split(".")[0]+".png")

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
