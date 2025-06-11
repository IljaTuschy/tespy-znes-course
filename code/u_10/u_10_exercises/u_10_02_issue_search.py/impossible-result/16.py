"""
Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, HeatExchanger
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

source_hot = Source("source hot")
source_cold = Source("source cold")

heatex = HeatExchanger("heat exchanger")

sink_hot = Sink("sink hot")
sink_cold = Sink("sink cold")

a1 = Connection(source_cold, "out1", heatex, "in1")
a2 = Connection(heatex, "out1", sink_cold, "in1")

b1 = Connection(source_hot, "out1", heatex, "in2")
b2 = Connection(heatex, "out2", sink_hot, "in1")

nw.add_conns(a1, a2, b1, b2)

a1.set_attr(fluid={"NH3": 1}, m=5, x=0.2)
a2.set_attr(x=1)

b1.set_attr(fluid={"water": 1}, T=30, p=1)
b2.set_attr(T=20)

heatex.set_attr(pr1=1, pr2=1, ttd_l=10)

nw.solve("design")
