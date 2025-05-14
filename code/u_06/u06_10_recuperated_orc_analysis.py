from fluprodia import FluidPropertyDiagram
import matplotlib.pyplot as plt
from tespy.networks import Network
from tespy.components import CycleCloser, Turbine, Pump, Source, Sink, HeatExchanger, MovingBoundaryHeatExchanger
from tespy.connections import Connection
from CoolProp.CoolProp import PropsSI as PSI


nw = Network(T_unit="C", p_unit="bar")

heat_source_in = Source("heat source inlet")
heat_source_out = Sink("heat source outlet")

cc = CycleCloser("cycle closer")
preheater = HeatExchanger("preheater")
evaporator = HeatExchanger("evaporator")
turbine = Turbine("turbine")
recuperator = HeatExchanger("recuperator")
condenser = MovingBoundaryHeatExchanger("condenser")
pump = Pump("feed pump")

cooling_in = Source("cooling inlet")
cooling_out = Sink("cooling outlet")

a1 = Connection(heat_source_in, "out1", evaporator, "in1", label="a1")
a2 = Connection(evaporator, "out1", preheater, "in1", label="a2")
a3 = Connection(preheater, "out1", heat_source_out, "in1", label="a3")

b1 = Connection(cc, "out1", turbine, "in1", label="b1")
b2 = Connection(turbine, "out1", recuperator, "in1", label="b2")
b3 = Connection(recuperator, "out1", condenser, "in1", label="b3")
b4 = Connection(condenser, "out1", pump, "in1", label="b4")
b5 = Connection(pump, "out1", recuperator, "in2", label="b5")
b6 = Connection(recuperator, "out2", preheater, "in2", label="b6")
b7 = Connection(preheater, "out2", evaporator, "in2", label="b7")
b0 = Connection(evaporator, "out2", cc, "in1", label="b0")

c1 = Connection(cooling_in, "out1", condenser, "in2", label="c1")
c2 = Connection(condenser, "out2", cooling_out, "in1", label="c2")

nw.add_conns(a1, a2, a3)
nw.add_conns(b1, b2, b3, b4, b5, b6, b7, b0)
nw.add_conns(c1, c2)

working_fluid = "Isopentane"

a1.set_attr(fluid={"water": 1}, p=10, T=160, m=100)

p_high = PSI("P", "T", 140 + 273.15, "Q", 1, working_fluid) / 1e5
p_low = PSI("P", "T", 50 + 273.15, "Q", 1, working_fluid) / 1e5

a2.set_attr(h0=140000)

b1.set_attr(fluid={working_fluid: 1}, x=1, T=140)
b3.set_attr(Td_bp=10, p0=p_low)
b4.set_attr(x=0)
b7.set_attr(x=0, p0=p_high)

c1.set_attr(fluid={"air": 1}, p=1, T=20)
c2.set_attr(T=35)

recuperator.set_attr(pr1=1, pr2=1)
preheater.set_attr(pr1=1, pr2=1)
evaporator.set_attr(pr1=1, pr2=1, ttd_l=5)
condenser.set_attr(pr2=1, pr1=1, td_pinch=5)
turbine.set_attr(eta_s=0.85)
pump.set_attr(eta_s=0.75)

nw.solve("design")

b3.set_attr(Td_bp=None)
recuperator.set_attr(eff_hot=0.5)

nw.solve("design")
nw.print_results()

power_output = abs(turbine.P.val) - pump.P.val
heat_input = abs(preheater.Q.val + evaporator.Q.val)
thermal_efficiency = power_output / heat_input
T_heat_out = a3.T.val
print(f"{power_output = }")
print(f"{thermal_efficiency = }")
print(f"{T_heat_out = }")

recuperator.set_attr(eff_hot=0.5)

T_hot_out_range = []
power_range = []
T_turbine_in_range = [150, 140, 130, 120, 110, 100, 90, 80]

for T in T_turbine_in_range:
    b1.set_attr(T=T)
    nw.solve("design")
    T_hot_out_range.append(a3.T.val)
    power_range.append(abs(turbine.P.val) - pump.P.val)

fig, ax = plt.subplots(2, sharex=True)

ax[0].plot(T_turbine_in_range, T_hot_out_range)
ax[1].plot(T_turbine_in_range, power_range)

ax[0].set_ylabel("Heat source outflow temperature °C")
ax[1].set_ylabel("Power generated in W")
ax[1].set_xlabel("Turbine inlet temperature in °C")

plt.tight_layout()
plt.show()

b1.set_attr(T=100)
T_hot_out_range = []
power_range = []
recup_eff_range = [0.05, 0.3, 0.5, 0.7, 0.95]

for eff in recup_eff_range:
    recuperator.set_attr(eff_hot=eff)
    nw.solve("design")
    T_hot_out_range.append(a3.T.val)
    power_range.append(abs(turbine.P.val) - pump.P.val)


fig, ax = plt.subplots(2)

ax[0].plot(recup_eff_range, T_hot_out_range)
ax[1].plot(recup_eff_range, power_range)

ax[0].set_ylabel("Heat source outflow temperature °C")
ax[1].set_ylabel("Power generated in W")
ax[1].set_xlabel("Recuperator effectiveness")

plt.tight_layout()
plt.show()

recuperator.set_attr(eff_hot=None)
a3.set_attr(T=80)
nw.solve("design")

print(
    "Recuperator effectiveness for a heat source outflow temperature of 80 °C "
    f"{recuperator.eff_hot.val}"
)
