"""
Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, Turbine
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="K", p_unit="bar")

source = Source("source")
turbine = Turbine("turbine")
sink = Sink("sink")

c1 = Connection(source, "out1", turbine, "in1")
c2 = Connection(turbine, "out1", sink, "in1")

nw.add_conns(c1, c2)

c1.set_attr(m=1, fluid={"air": 1}, T=50, p=10)
c2.set_attr(p=1)

turbine.set_attr(eta_s=0.9)

nw.solve("design")
