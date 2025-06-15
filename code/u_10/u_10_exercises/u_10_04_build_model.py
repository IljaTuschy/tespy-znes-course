# Flowsheet + data table
# Calculate specific outcome (e.g. COP, eta_th, ...)
# possible examples
# - pressurized air system with intermediate cooling
# - heat exchanger with both sides, one side with a pump for flow through, one
#   side with pump to pressurize system
# - flash process using pump, heater to saturated water, valve throttle to original pressure
#   calculate steam and liquid mass flow at valve exit

from tespy.components import Source, Sink, Compressor, SimpleHeatExchanger
from tespy.networks import Network
from tespy.connections import Connection


nw = Network(T_unit="C", p_unit="bar")

ambient_air = Source("ambient air")
pressurized_air = Sink("pressurized air")

compressor_1 = Compressor("compressor stage 1")
compressor_2 = Compressor("compressor stage 2")
cooler_1 = SimpleHeatExchanger("cooler 1")
cooler_2 = SimpleHeatExchanger("cooler 2")

c1 = Connection(ambient_air, "out1", compressor_1, "in1", label="1")
c2 = Connection(compressor_1, "out1", cooler_1, "in1", label="2")
c3 = Connection(cooler_1, "out1", compressor_2, "in1", label="3")
c4 = Connection(compressor_2, "out1", cooler_2, "in1", label="4")
c5 = Connection(cooler_2, "out1", pressurized_air, "in1", label="5")

nw.add_conns(c1, c2, c3, c4, c5)

cooler_1.set_attr(dp=0.05)
cooler_2.set_attr(dp=0.05)

compressor_1.set_attr(eta_s=0.8)
compressor_2.set_attr(eta_s=0.8)

c1.set_attr(fluid={"air": 1}, m=5, p=1, T=25)
c3.set_attr(p=4, T=40)
c5.set_attr(p=10, T=40)

nw.solve("design")


import numpy as np

pressure_range = np.linspace(2, 9)
power_demand_range = []

for p in pressure_range:
    c3.set_attr(p=p)
    nw.solve("design")
    power_demand_range += [(compressor_1.P.val + compressor_2.P.val) / 1e6]


from matplotlib import pyplot as plt


fig, ax = plt.subplots(1)

ax.scatter(pressure_range, power_demand_range)

ax.set_ylabel("power demand in MW")
ax.set_ylabel("intermediate pressure in bar")

plt.show()
