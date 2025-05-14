from tespy.networks import Network
from tespy.components import CycleCloser, Turbine, Pump, Source, Sink, HeatExchanger, MovingBoundaryHeatExchanger
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
condenser = MovingBoundaryHeatExchanger("condenser")
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

a1.set_attr(fluid={"water": 1}, p=10, T=160, m=100)

a2.set_attr(h0=140000)  # we need to provide a starting value because the water is in two-phase otherwise

b1.set_attr(fluid={working_fluid: 1}, x=1, T=140)
b3.set_attr(x=0, p0=PSI("P", "T", 35 + 273.15, "Q", 0, working_fluid) / 1e5)
b5.set_attr(x=0, p0=PSI("P", "T", 140 + 273.15, "Q", 0, working_fluid) / 1e5)  # prevent the PQ call with p > p_crit

c1.set_attr(fluid={"air": 1}, p=1, T=20)
c2.set_attr(T=35)

preheater.set_attr(pr1=1, pr2=1)
evaporator.set_attr(pr1=1, pr2=1, ttd_l=5)
condenser.set_attr(pr2=1, pr1=1, td_pinch=5)

b2.set_attr(h=PSI("H", "T", 35 + 273.15, "Q", 1.0, working_fluid) * 1.1)
pump.set_attr(eta_s=0.75)

nw.solve("design")

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
