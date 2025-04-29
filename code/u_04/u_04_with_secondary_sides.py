from tespy.components import HeatExchanger, Source, Sink, Valve, CycleCloser, Compressor
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI


nw = Network(T_unit="C", p_unit="bar")

ev = HeatExchanger("evaporator")
cp = Compressor("compressor")
cd = HeatExchanger("condenser")
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

# Specifications are not necessarily reasonable here. We want to connect the
# evaporation temperature to the air temperature and the condensation
# temperature to the water temperature

ev.set_attr(ttd_l=5)
c2.set_attr(T=None)

cd.set_attr(ttd_l=10)
c4.set_attr(T=None)

nw.solve("design")
nw.print_results()

condensation_h = [
    c3.h.val_SI, PropsSI("H", "P", c3.p.val_SI, "Q", 1, "R290"), c4.h.val_SI
]
condensation_Q = [(c3.h.val_SI - h)* c3.m.val_SI for h in condensation_h]
condensation_T = [PropsSI("T", "P", c3.p.val_SI, "H", h, "R290") - 273.15 for h in condensation_h]
water_heating_h = [c11.h.val_SI + Q / c11.m.val_SI for Q in condensation_Q]
water_heating_T = [
    PropsSI("T", "P", c11.p.val_SI, "H", h, "water") - 273.15 for h in water_heating_h
]

evaporation_h = [c1.h.val_SI, c2.h.val_SI]
evaporation_Q = [(c2.h.val_SI - h) for h in evaporation_h]
evaporation_T = [PropsSI("T", "P", c1.p.val_SI, "H", h, "R290") - 273.15 for h in evaporation_h]
air_cooling_h = [
    c21.h.val_SI - Q / c22.m.val_SI for Q in evaporation_Q
]
air_cooling_T = [
    PropsSI("T", "P", c12.p.val_SI, "H", h, "air") - 273.15 for h in air_cooling_h
]

# In the plot below we can see, that there is a pinch violation in the
# condesation part. tespy does not warn you of this, if it happens inside a
# regiular heat exchanger!

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, sharey=True)

ax[0].plot([abs(cd.Q.val) - Q for Q in condensation_Q], condensation_T, label="R290")
ax[0].plot(condensation_Q, water_heating_T, label="air")

ax[0].set_ylabel("Temperature in °C")
ax[0].set_xlabel("Heat transferred in W")
ax[0].legend()

ax[1].plot(evaporation_Q, evaporation_T, label="R290")
ax[1].plot([abs(ev.Q.val) - Q for Q in evaporation_Q], air_cooling_T, label="air")
ax[1].legend()

ax[1].set_xlabel("Heat transferred in W")
plt.show()

# To fix this, we have to modify the condenser terminal temperature difference

cd.set_attr(ttd_l=20)

nw.solve("design")
nw.print_results()

condensation_h = [
    c3.h.val_SI, PropsSI("H", "P", c3.p.val_SI, "Q", 1, "R290"), c4.h.val_SI
]
condensation_Q = [(c3.h.val_SI - h)* c3.m.val_SI for h in condensation_h]
condensation_T = [PropsSI("T", "P", c3.p.val_SI, "H", h, "R290") - 273.15 for h in condensation_h]
water_heating_h = [c11.h.val_SI + Q / c11.m.val_SI for Q in condensation_Q]
water_heating_T = [
    PropsSI("T", "P", c11.p.val_SI, "H", h, "water") - 273.15 for h in water_heating_h
]

evaporation_h = [c1.h.val_SI, c2.h.val_SI]
evaporation_Q = [(c2.h.val_SI - h) for h in evaporation_h]
evaporation_T = [PropsSI("T", "P", c1.p.val_SI, "H", h, "R290") - 273.15 for h in evaporation_h]
air_cooling_h = [
    c21.h.val_SI - Q / c22.m.val_SI for Q in evaporation_Q
]
air_cooling_T = [
    PropsSI("T", "P", c12.p.val_SI, "H", h, "air") - 273.15 for h in air_cooling_h
]

fig, ax = plt.subplots(1, 2, sharey=True)

ax[0].plot([abs(cd.Q.val) - Q for Q in condensation_Q], condensation_T, label="R290")
ax[0].plot(condensation_Q, water_heating_T, label="water")

ax[0].set_ylabel("Temperature in °C")
ax[0].set_xlabel("Heat transferred in W")
ax[0].legend()

ax[1].plot(evaporation_Q, evaporation_T, label="R290")
ax[1].plot([abs(ev.Q.val) - Q for Q in evaporation_Q], air_cooling_T, label="air")
ax[1].legend()

ax[1].set_xlabel("Heat transferred in W")
plt.show()
