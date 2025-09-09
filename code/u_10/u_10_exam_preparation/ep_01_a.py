"""
Script to calculate the 
power of a compressor
with known efficiency
compressing air from ambient
condition to a given
pressure in a tank 

Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, Compressor
from tespy.connections import Connection
from tespy.networks import Network

# create network and define unit system
nw = Network(p_unit='bar', T_unit='C')

# define topology
# create components
amb = Source('ambience')
comp = Compressor('air compressor')
tank = Sink('pressurized air tank')

# set connections:
# c1: compressor inlet
# c2: compressor outlet
c1 = Connection(amb, 'out1', comp, 'in1', 'c1')
c2 = Connection(comp, 'out1', tank, 'in1', 'c2')
nw.add_conns(c1, c2)

# parametrize network:
# air inlet conditions
c1.set_attr(fluid='air', m=1, p=1, T=20)
# outlet pressure
c2.set_attr(p=10)
# compressor efficiency
comp.set_attr(eta_s=0.9)

# simulate in design mode 
nw.solve('design')
