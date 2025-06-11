"""
Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, Turbine
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

source = Source("source")
turbine = Turbine("turbine")
sink = Sink("sink")

c1 = Connection(source, "out1", turbine, "in1")
c2 = Connection(turbine, "out1", sink, "in1")

nw.add_conns(c1, c2)

c1.set_attr(fluid={"water": 1}, m=1, T=500, p=100)
c2.set_attr(x=0.95, p=10)

nw.solve("design")
