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

# Specifications are not necessarily reasonable here. We want to connect the
# evaporation temperature to the air temperature and the condensation
# temperature to the water temperature

ev.set_attr(td_pinch=5)
c2.set_attr(T=None)

# we can directly impose the pinch temperature difference with this component
cd.set_attr(td_pinch=5)
c4.set_attr(T=None)

nw.solve("design")
nw.print_results()

Q_steps_cond, T_steps_hot_cond, T_steps_cold_cond, _, _ = cd.calc_sections()
Q_steps_ev, T_steps_hot_ev, T_steps_cold_ev, _, _ = ev.calc_sections()

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, sharey=True)

ax[0].plot(Q_steps_cond, T_steps_hot_cond, label="R290")
ax[0].plot(Q_steps_cond, T_steps_cold_cond, label="water")

ax[0].set_ylabel("Temperature in °C")
ax[0].set_xlabel("Heat transferred in W")
ax[0].legend()

ax[1].plot(Q_steps_ev, T_steps_hot_ev, label="R290")
ax[1].plot(Q_steps_ev, T_steps_cold_ev, label="air")
ax[1].legend()

ax[1].set_xlabel("Heat transferred in W")
plt.show()
