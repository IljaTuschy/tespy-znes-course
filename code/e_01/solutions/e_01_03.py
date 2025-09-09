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
b) a sketch of the heat balace diagram
'''
from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Source,
    Sink,
    Pump,
    SimpleHeatExchanger,
    Merge
)
import numpy as np
import matplotlib.pyplot as plt
n = Network()
a = Source('a')
b = SimpleHeatExchanger('b')
c = Merge('c')
d = Sink('d')
e = Source('e')
f = Pump('f')
A = Connection(a, 'out1', b, 'in1', 'A')
B = Connection(b, 'out1', c, 'in1', 'B')
C = Connection(c, 'out1', d, 'in1', 'C')
D = Connection(e, 'out1', f, 'in1', 'D')
E = Connection(f, 'out1', c, 'in2', 'E')
n.add_conns(A, B, C, D, E)
A.set_attr(fluid={'water':1}, p=10e5, T=273.15+20)
B.set_attr(x=0)
D.set_attr(fluid={'water':1}, p=1e5, T=273.15+20)
b.set_attr(pr=1)
f.set_attr(eta_s=1)
for x in (10, 20, 30, 40):
    A.set_attr(m=x)
    y = np.linspace(40, 100, 20)
    r = np.empty([20])
    i = 0
    for z in y:
        C.set_attr(T=273.15+z)
        n.set_attr(iterinfo=False)
        n.solve('design')
        r[i]=f.get_attr('P').val
        i += 1
    plt.plot(y,r)
plt.show()
