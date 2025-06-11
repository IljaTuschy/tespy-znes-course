"""
Find the issue with the code below and fix it.
"""

from tespy.components import Source, Sink, Merge
from tespy.connections import Connection
from tespy.networks import Network

nw = Network()

source1 = Source("source1")
source2 = Source("source2")
merge = Merge("merge")
sink = Sink("sink")

c1 = Connection(source1, "out1", merge, "in1")
c2 = Connection(source2, "out1", merge, "in2")
c3 = Connection(merge, "out1", sink, "in1")

nw.add_conns(c1, c2, c3)

c1.set_attr(fluid={"water": 1}, p=1e5, T=293.15, m=10)
c2.set_attr(fluid={"water": 1}, m=5, T=293.15, p=1e5)

nw.solve("design")
