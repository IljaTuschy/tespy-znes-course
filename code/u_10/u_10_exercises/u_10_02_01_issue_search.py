# List of potential issues
# FLUIDS
# - non-specified fluid composition
# - fluid just as string
# - mass fraction of fluids not adding up to 1 or larger than 1

from tespy.components import Source, Sink
from tespy.connections import Connection
from tespy.networks import Network


nw = Network()

c1 = Connection(Source("test"), "out1", Sink("test2"), "in1")

nw.add_conns(c1)

# - c1.set_attr(m=1, p=1e5, T=293.15)
# - c1.set_attr(m=1, p=1e5, T=293.15, fluid={"N2"})
# - c1.set_attr(m=1, p=1e5, T=293.15, fluid="N2")
# - c1.set_attr(m=1, p=1e5, T=293.15, fluid={"N2": 0.75, "O2": 0.30})

# nw.solve("design")

# INCORRECT NUMBER OF SPECIFICATIONS
from tespy.components import Merge

nw = Network()

merge = Merge("merge")
c1 = Connection(Source("test"), "out1", merge, "in1")
c2 = Connection(Source("test2"), "out1", merge, "in2")
c3 = Connection(merge, "out1", Sink("test3"), "in1")

nw.add_conns(c1, c2, c3)

# TOO MANY PARAMETERS
# c1.set_attr(fluid={"water": 1}, p=1e5, T=293.15, m=10)
# c2.set_attr(fluid={"water": 1}, m=5, T=293.15, p=1e5)
# TOO FEW PARAMETERS
# c1.set_attr(fluid={"water": 1}, T=293.15, m=10)
# c2.set_attr(fluid={"water": 1}, m=5, T=293.15)

# nw.solve("design")

# CORRECT NUMBER BUT LINEAR DEPENDENCY

# c1.set_attr(fluid={"water": 1}, p=1e5, T=293.15, m=10)
# c2.set_attr(fluid={"water": 1}, p=2e5, T=293.15)

# nw.solve("design")

# UNITS DO NOT MATCH

nw = Network(T_unit="K", p_unit="bar")

c1 = Connection(Source("test"), "out1", Sink("test2"), "in1")

nw.add_conns(c1)

# c1.set_attr(m=1, fluid={"water": 1}, T=50, x=1)
# c1.set_attr(m=1, fluid={"water": 1}, p=1e5, x=1)

# nw.solve("design")

# WRONG CONNECTION SETUP

# Connection(Sink("sink"), "out1", Source("source"), "in1")
# Connection(Source("source"), "out2", Sink("sink"), "in1")

# FORGOT TO ADD CONNECTION TO NETWORK

from tespy.components import SimpleHeatExchanger

# nw = Network()

# shex = SimpleHeatExchanger("shex")

# c1 = Connection(Source("source"), "out1", shex, "in1")
# c2 = Connection(shex, "out1", Sink("sink"), "in1")

# nw.add_conns(c1)

# nw.solve("design")

# WRONG CONNECTION SETUP

# shex = SimpleHeatExchanger("test")
# shex.set_attr(pr1=0.9)

# STARTING VALUE ISSUE
