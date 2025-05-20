from tespy.components import Source, Sink, HeatExchanger, Pump, SimpleHeatExchanger, Turbine, CycleCloser
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

source_cw = Source("cooling water source")
sink_cw = Sink("cooling water sink")

turbine = Turbine("steam turbine")
condenser = HeatExchanger("condenser")
pump = Pump("feed pump")
steam_generator = SimpleHeatExchanger("steam generator")
cc = CycleCloser("cycle closer")

c1 = Connection(cc, "out1", turbine, "in1", label="c1")
c2 = Connection(turbine, "out1", condenser, "in1", label="c2")
c3 = Connection(condenser, "out1", pump, "in1", label="c3")
c4 = Connection(pump, "out1", steam_generator, "in1", label="c4")
c0 = Connection(steam_generator, "out1", cc, "in1", label="c0")

a1 = Connection(source_cw, "out1", condenser, "in2", label="a1")
a2 = Connection(condenser, "out2", sink_cw, "in1", label="a2")

nw.add_conns(c1, c2, c3, c4, c0, a1, a2)

c1.set_attr(fluid={"water": 1}, m=10, p=80, T=550)
c3.set_attr(x=0, T=40)

a1.set_attr(fluid={"water": 1}, p=1, T=25)
a2.set_attr(T=35)

turbine.set_attr(eta_s=0.9)
pump.set_attr(eta_s=0.75)
condenser.set_attr(dp1=0, dp2=0)
steam_generator.set_attr(dp=0)

nw.solve("design")
nw.print_results()
nw.save("rankine_design.json")

turbine.set_attr(design=["eta_s"], offdesign=["eta_s_char", "cone"])
c1.set_attr(design=["p"])

condenser.set_attr(offdesign=["kA"])
c3.set_attr(design=["T"])

nw.solve("offdesign", design_path="rankine_design.json")
nw.set_attr(iterinfo=False)


import matplotlib.pyplot as plt

import numpy as np


heat_in_range = []
power_range = []
m_range = np.linspace(5, 12)
for m in m_range:
    c1.set_attr(m=m)
    nw.solve("offdesign", design_path="rankine_design.json")
    heat_in_range.append(steam_generator.Q.val)
    power_range.append(abs(turbine.P.val) - pump.P.val)

heat_in_range = np.array(heat_in_range) / 1e6
power_range = np.array(power_range) / 1e6
thermal_efficiency_range = power_range / heat_in_range * 100

fig, ax = plt.subplots(2)

ax[0].plot(power_range, heat_in_range)
ax[1].plot(power_range, thermal_efficiency_range)

ax[0].set_ylabel("Thermal input in MW")
ax[1].set_ylabel("Thermal efficiency in %")
ax[1].set_xlabel("Power in MW")

plt.tight_layout()
plt.show()
