from tespy.networks import Network
from tespy.components import CycleCloser, Turbine, Pump, Source, Sink, HeatExchanger
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as PSI
import numpy as np


nw = Network(T_unit="C", p_unit="bar")

heat_source_in = Source("heat source inlet")
heat_source_out = Sink("heat source outlet")

cc = CycleCloser("cycle closer")
preheater = HeatExchanger("preheater")
evaporator = HeatExchanger("evaporator")
turbine = Turbine("turbine")
condenser = HeatExchanger("condenser")
pump = Pump("feed pump")

cooling_in = Source("cooling inlet")
cooling_out = Sink("cooling outlet")

a1 = Connection(heat_source_in, "out1", evaporator, "in1", label="a1")
a2 = Connection(evaporator, "out1", preheater, "in1", label="a2")
a3 = Connection(preheater, "out1", heat_source_out, "in1", label="a3")

b1 = Connection(cc, "out1", turbine, "in1", label="b1")
b2 = Connection(turbine, "out1", condenser, "in1", label="b2")
b3 = Connection(condenser, "out1", pump, "in1", label="b3")
b4 = Connection(pump, "out1", preheater, "in2", label="b4")
b5 = Connection(preheater, "out2", evaporator, "in2", label="b5")
b0 = Connection(evaporator, "out2", cc, "in1", label="b0")

c1 = Connection(cooling_in, "out1", condenser, "in2", label="c1")
c2 = Connection(condenser, "out2", cooling_out, "in1", label="c2")

nw.add_conns(a1, a2, a3)
nw.add_conns(b1, b2, b3, b4, b5, b0)
nw.add_conns(c1, c2)

working_fluid = "Isopentane"

a1.set_attr(fluid={"air": 1}, p=1, T=160, m=100)

b0.set_attr(fluid={working_fluid: 1}, x=1, T=140)

b3.set_attr(x=0, p0=PSI("P", "T", 35 + 273.15, "Q", 0, working_fluid) / 1e5)
b5.set_attr(x=0, p0=PSI("P", "T", 140 + 273.15, "Q", 0, working_fluid) / 1e5)  # prevent the PQ call with p > p_crit

c1.set_attr(fluid={"air": 1}, p=1, T=20)
c2.set_attr(T=35)

preheater.set_attr(pr1=1, pr2=1)
evaporator.set_attr(pr1=1, pr2=1, ttd_l=5)
condenser.set_attr(pr2=1, pr1=1, ttd_l=15)

# we will not use the turbine efficiency as input here, instead turbine
# outlet enthalpy for the initial solve
b2.set_attr(h=PSI("H", "T", 35 + 273.15, "Q", 0.9, working_fluid))
pump.set_attr(eta_s=0.75)

nw.solve("design")

# now we can set to final parameters
turbine.set_attr(eta_s=0.85)
b2.set_attr(h=None)

nw.solve("design")
nw.print_results()

power_output = abs(turbine.P.val) - pump.P.val
heat_input = abs(preheater.Q.val + evaporator.Q.val)
thermal_efficiency = power_output / heat_input
T_heat_out = a3.T.val
print(f"{power_output = }")
print(f"{thermal_efficiency = }")
print(f"{T_heat_out = }")


from matplotlib import pyplot as plt

fig, ax = plt.subplots(1)


dome_T = np.linspace(273.15, PSI("Tcrit", working_fluid))
dome_Q_0_s = PSI("S", "T", dome_T, "Q", 0, working_fluid)
dome_Q_1_s = PSI("S", "T", dome_T, "Q", 1, working_fluid)

ax.plot(dome_Q_0_s, dome_T, color="black")
ax.plot(dome_Q_1_s, dome_T, color="black")

process_T = [c.T.val_SI for c in [b1, b2, b3, b4, b5, b0]]
process_s = [c.s.val_SI for c in [b1, b2, b3, b4, b5, b0]]

T_sat_2 = b3.T.val_SI
s_sat_2 = PSI("S", "P", b2.p.val_SI, "Q", 1, working_fluid)

process_T.insert(2, T_sat_2)
process_s.insert(2, s_sat_2)

ax.plot(process_s, process_T)

plt.tight_layout()
plt.show()

h_steps_hot = [b2.h.val_SI, PSI("H", "P", b2.p.val_SI, "Q", 1, working_fluid), b3.h.val_SI]
T_steps_hot = [PSI("T", "P", b2.p.val_SI, "H", h, working_fluid) for h in h_steps_hot]
delta_h_steps = [0, h_steps_hot[0] - h_steps_hot[1], h_steps_hot[1] - h_steps_hot[2]]
Q_steps = [dh * b2.m.val_SI for dh in delta_h_steps]

h_steps_cold = [c2.h.val_SI - Q / c1.m.val_SI for Q in Q_steps]

T_steps_cold = [PSI("T", "P", c1.p.val_SI, "H", h, "air") for h in h_steps_cold]

fig, ax = plt.subplots(1)

ax.plot(Q_steps, T_steps_hot, "x-")
ax.plot(Q_steps, T_steps_cold, "o-")

plt.tight_layout()
plt.show()
