"""
Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, SimpleHeatExchanger
from tespy.connections import Connection
from tespy.networks import Network

nw = Network(p_unit="bar", T_unit="C")

heater = SimpleHeatExchanger("heater")

c1 = Connection(Source("source"), "out1", heater, "in1")
c2 = Connection(heater, "out1", Sink("sink"), "in1")

nw.add_conns(c1)

c1.set_attr(fluid={"R32": 1}, p=10, T=25)
c2.set_attr(T=50)

heater.set_attr(Q=1e6, pr=1)

nw.solve("design")
