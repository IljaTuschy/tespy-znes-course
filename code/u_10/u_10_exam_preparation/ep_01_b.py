"""
Script to calculate the 
outlet conditions of a 
piping for R134a after
a known pressure drop

Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, Pipe
from tespy.connections import Connection
from tespy.networks import Network

# create network and switch off iteration info
nw = Network(iterinfo=False)

# define topology
# create components
source = Source('R134a source')
pipe = Pipe('piping')
sink = Sink('R134a sink')

# set connections:
# c1: piping inlet
# c2: piping outlet
c1 = Connection(source, 'out1', pipe, 'in1', 'c1')
c2 = Connection(pipe, 'out1', sink, 'in1', 'c2')
nw.add_conns(c1, c2)

# parametrize network:
# R134a inlet conditions
c1.set_attr(fluid={'R134a':1}, m=1, p=1e5, T=273.15+20)
# outlet pressure
c2.set_attr(p=0.9e5)
# piping component data
pipe.set_attr(pr=0.9, Q=0)

# solve network and print results for design calculation
nw.solve('design')
nw.print_results()
