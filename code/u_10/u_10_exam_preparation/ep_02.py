'''
This code is hard to read as
there are neither comments nor 
self explaining variable names.

Please identify what the script
is for and add comments to make
the code more readable. You may even
change variable names

Additionally please draw a
sketch denominating all components
and connections.

You are free to test, use and modify 
the code of the exercise.

Your result needs to be 
a) a commented python script as a file or text
b) a file of any type holding the sketch
'''
from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Source,
    Sink,
    Turbine,
    SimpleHeatExchanger,
    Splitter
)
import numpy as np
import matplotlib.pyplot as plt
n = Network()
a = Source('a')
b = Turbine('b')
c = Splitter('c')
d = Turbine('d')
e = Sink('e')
f = SimpleHeatExchanger('f')
g = Sink('g')
A = Connection(a, 'out1', b, 'in1', 'A')
B = Connection(b, 'out1', c, 'in1', 'B')
C = Connection(c, 'out1', d, 'in1', 'C')
D = Connection(d, 'out1', e, 'in1', 'D')
E = Connection(c, 'out2', f, 'in1', 'E')
F = Connection(f, 'out1', g, 'in1', 'F')
n.add_conns(A, B, C, D, E, F)
A.set_attr(fluid={'water':1}, m=10, p=100e5, T=273.15+500)
D.set_attr(p=0.1e5)
E.set_attr(m=5)
F.set_attr(x=0)
b.set_attr(eta_s=0.9)
d.set_attr(eta_s=0.9)
f.set_attr(pr=0.9)
x = np.linspace(5,25, 21)
y = np.empty([21])
z = np.empty([21])
i = 0
for u in x:
    B.set_attr(p=u*1e5)
    n.set_attr(iterinfo=False)
    n.solve('design')
    y[i] = (-b.get_attr('P').val - d.get_attr('P').val)*1e-6
    z[i] = -f.get_attr('Q').val*1e-6
    i +=1
plt.plot(x,y)
plt.plot(x,z)
plt.show()
