"""
This module calculates the
mass flow needed to provide
a defined power output of a 
steam turbine working between
two steam lines

Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, Turbine
from tespy.connections import Connection
from tespy.networks import Network

# create network and set unit system
nw = Network(T_unit="C", p_unit="bar")

# define topology
source = Source("high pressure steam line")
turbine = Turbine("turbine")
sink = Sink("low pressure steam line")

c1 = Connection(source, "out1", turbine, "in1", "turbine live steam")
c2 = Connection(turbine, "out1", sink, "in1", "turbine exhaust steam")

nw.add_conns(c1, c2)

# parametrize
# high pressure steam line conditions and low pressure steam line pressure
c1.set_attr(fluid={"water": 1}, T=500, p=100)
c2.set_attr(p=10)

# turbine efficiency and power output
turbine.set_attr(eta_s=0.9, P=1e6)

# simulate and print results
nw.solve("design")
nw.print_results()
