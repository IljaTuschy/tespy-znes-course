from tespy.components import MovingBoundaryHeatExchanger, Source, Sink, Valve, CycleCloser, Compressor
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI


nw = Network(T_unit="C", p_unit="bar")

ev = MovingBoundaryHeatExchanger("evaporator")
cp = Compressor("compressor")
cd = MovingBoundaryHeatExchanger("condenser")
va = Valve("valve")
cc = CycleCloser("cycle closer")

water_cold = Source("Cold water")
water_hot = Sink("Hot water")
air_intake = Source("Air intake")
air_outlet = Sink("Air outlet")

c1 = Connection(cc, "out1", ev, "in2", label="1")
c2 = Connection(ev, "out2", cp, "in1", label="2")
c3 = Connection(cp, "out1", cd, "in1", label="3")
c4 = Connection(cd, "out1", va, "in1", label="4")
c0 = Connection(va, "out1", cc, "in1", label="0")

nw.add_conns(c1, c2, c3, c4, c0)

c11 = Connection(water_cold, "out1", cd, "in2", label="11")
c12 = Connection(cd, "out2", water_hot, "in1", label="12")

c21 = Connection(air_intake, "out1", ev, "in1", label="21")
c22 = Connection(ev, "out1", air_outlet, "in1", label="22")

nw.add_conns(c11, c12, c21, c22)

c1.set_attr(fluid={"R290": 1}, m=1)
c2.set_attr(T=15, x=1)

c4.set_attr(T=60, x=0)

ev.set_attr(pr1=1, pr2=1)
cp.set_attr(eta_s=0.85)
cd.set_attr(pr1=1, pr2=1)

c11.set_attr(fluid={"water": 1}, T=35, p=1)
c12.set_attr(T=50)

c21.set_attr(fluid={"air": 1}, T=20, p=1, m=10)

nw.solve("design")

# we still perform solving in two steps, the first run is to generate
# a good guess as starting values for pressure and enthalpy in the working
# fluid cycle, this second run is to ensure no pinch is violated
ev.set_attr(td_pinch=5)
c2.set_attr(T=None)
cd.set_attr(td_pinch=5)
c4.set_attr(T=None)

nw.solve("design")
nw.print_results()

import numpy as np

# iterate through a range of ambient temperature (from -20 to 25 in steps of)
# 2 °C
T_ambient_range = np.arange(-20, 25, 2)
cop = []

for T in T_ambient_range:
    c21.set_attr(T=T)
    nw.solve("design")
    cop += [abs(cd.Q.val) / cp.P.val]


from matplotlib import pyplot as plt

fig, ax = plt.subplots(1)

ax.scatter(T_ambient_range, cop)
ax.set_ylabel("COP of the heat pump")
ax.set_xlabel("Ambient temperature in °C")

plt.tight_layout()
plt.show()

# change back the air temperature where it originally was
# and then iterate through different heating temperature values
c21.set_attr(T=20)
T_heating_range = np.arange(40, 80, 2)
cop = []

for T in T_heating_range:
    c12.set_attr(T=T)
    nw.solve("design")
    cop += [abs(cd.Q.val) / cp.P.val]

fig, ax = plt.subplots(1)

ax.scatter(T_heating_range, cop)
ax.set_ylabel("COP of the heat pump")
ax.set_xlabel("Heating temperatur in °C")

plt.tight_layout()
plt.show()
