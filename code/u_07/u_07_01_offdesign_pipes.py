'''
script to model components with respect to
design and off-design using the TESPy component 

pipe

belongs to

Unit 07: Design and Offdesign Performance

'''

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Source,
    Pipe,
    Sink
)

import numpy as np
import matplotlib.pyplot as plt

# define piping network
pn = Network()

# create components without parametrization
air_in = Source('air inlet')
pip = Pipe('pipe')
air_out = Sink('air outlet')

# set up topology
c01 = Connection(air_in, 'out1', pip, 'in1', 'c01')
c02 = Connection(pip, 'out1', air_out, 'in1', 'c02')

pn.add_conns(c01, c02)

# parametrize
fluid = {'Air': 1} 
p_in = 5e5 #inlet pressure in Pa
T_in = 298.15 #inlet temperature in K
m = 1 #air mass flow in kg/s

c01.set_attr(fluid=fluid, p=p_in, T=T_in, m=m)
pip.set_attr(Q=0) # assume adiabatic piping

pip.set_attr(dp=0.02e5, ks=0.00005, L=200, D='var')

pn.solve(mode='design')
pn.print_results()

d=pip.get_attr('D').val
print(d)

pip.set_attr(dp=None)
pip.set_attr(D=d)

pn.solve(mode='design')
pn.print_results()

m_range = np.linspace(m*0.5, m*2, 20)
dp_range = np.empty([20])

pn.set_attr(iterinfo=False)
i=0
for m_new in m_range:
    c01.set_attr(m=m_new)
    pn.solve(mode='design')
    dp_range[i]=pip.get_attr('dp').val
    i +=1

print(m_range)
print(dp_range)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(m_range, dp_range)
plt.show()
