from tespy.components import Source, Sink, HeatExchanger
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

so_steam = Source("steam")
si_cond = Sink("condensate")
so_cw = Source("cooling water source")
si_cw = Sink("cooling water sink")
condenser = HeatExchanger("condenser")

a1 = Connection(so_steam, "out1", condenser, "in1", label="a1")
a2 = Connection(condenser, "out1", si_cond, "in1", label="a2")

b1 = Connection(so_cw, "out1", condenser, "in2", label="b1")
b2 = Connection(condenser, "out2", si_cw, "in1", label="b2")

nw.add_conns(a1, a2, b1, b2)

a1.set_attr(fluid={"water": 1}, m=1, x=1, p=0.1)
a2.set_attr(x=0)

b1.set_attr(fluid={"water": 1}, p=1, T=20)
b2.set_attr(T=30)

condenser.set_attr(dp1=0, dp2=0)

nw.solve("design")
nw.print_results()
nw.save("condenser_design.json")

# test, if the specifications work
a1.set_attr(design=["p"])
condenser.set_attr(offdesign=["kA"])

nw.solve("offdesign", design_path="condenser_design.json")


import numpy as np
from matplotlib import pyplot as plt


nw.set_attr(iterinfo=False)
m_cond_range = np.linspace(0.3, 1.5)
p_cond_range = []
for m in m_cond_range:
    a1.set_attr(m=m)
    nw.solve("offdesign", design_path="condenser_design.json")
    p_cond_range.append(a1.p.val)

p_cond_range = np.array(p_cond_range)

fig, ax = plt.subplots(1)

ax.scatter(m_cond_range, p_cond_range)

ax.set_ylabel("Condensation pressure in bar")
ax.set_xlabel("Condensate mass flow in kg/s")

plt.tight_layout()
plt.show()
