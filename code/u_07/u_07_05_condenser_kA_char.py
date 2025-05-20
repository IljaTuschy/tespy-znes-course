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


from tespy.tools import CharLine
import numpy as np


condensation_m_ratio = np.linspace(0, 3)
condensation_kA_char = condensation_m_ratio ** 0.45
char1=CharLine(x=condensation_m_ratio, y=condensation_kA_char)

cooling_m_ratio = np.linspace(0, 3)
cooling_kA_char = np.ones(len(cooling_m_ratio))
char2=CharLine(x=condensation_m_ratio, y=condensation_kA_char)

# apply the generated data to the component
condenser.set_attr(kA_char1=char1, kA_char2=char2)
condenser.set_attr(offdesign=["kA_char"])
a1.set_attr(design=["p"])

nw.solve("offdesign", design_path="condenser_design.json")


from matplotlib import pyplot as plt


nw.set_attr(iterinfo=False)
m_cond_range = np.linspace(0.3, 1.5)
p_cond_range = []
kA_range = []
for m in m_cond_range:
    a1.set_attr(m=m)
    nw.solve("offdesign", design_path="condenser_design.json")
    p_cond_range.append(a1.p.val)
    kA_range.append(condenser.kA.val)

fig, ax = plt.subplots(2, sharex=True)

ax[0].scatter(m_cond_range, p_cond_range)
ax[1].scatter(m_cond_range, kA_range)

ax[0].set_ylabel("Condensation pressure in bar")
ax[1].set_ylabel("Condenser kA in W/K")
ax[1].set_xlabel("Condensate mass flow in kg/s")

plt.tight_layout()
plt.show()
