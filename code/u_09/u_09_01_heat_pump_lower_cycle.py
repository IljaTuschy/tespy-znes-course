from tespy.components import Source, Sink, MovingBoundaryHeatExchanger, Compressor, Valve, CycleCloser, SimpleHeatExchanger
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

so_air = Source("air inlet")
si_air = Sink("air outlet")

cc_low = CycleCloser("cc lower cycle")
compressor_low = Compressor("compressor lower cycle")
internal_heat_exchanger = SimpleHeatExchanger("internal heat exchanger")
valve_low = Valve("valve lower cycle")
evaporator = MovingBoundaryHeatExchanger("evaporator")

a1 = Connection(so_air, "out1", evaporator, "in1", label="a1")
a2 = Connection(evaporator, "out1", si_air, "in1", label="a2")

b1 = Connection(cc_low, "out1", compressor_low, "in1", label="b1")
b2 = Connection(compressor_low, "out1", internal_heat_exchanger, "in1", label="b2")
b3 = Connection(internal_heat_exchanger, "out1", valve_low, "in1", label="b3")
b4 = Connection(valve_low, "out1", evaporator, "in2", label="b4")
b0 = Connection(evaporator, "out2", cc_low, "in1", label="b0")

nw.add_conns(a1, a2, b0, b1, b2, b3, b4)

a1.set_attr(fluid={"air": 1}, p=1, T=20, m=10)
a2.set_attr(T=10)

b1.set_attr(fluid={"R245FA": 1}, x=1, T=0)
b3.set_attr(x=0, T=60)

evaporator.set_attr(pr1=1, pr2=1)
compressor_low.set_attr(eta_s=0.9)
internal_heat_exchanger.set_attr(pr=1)

nw.solve("design")

b1.set_attr(T=None)
evaporator.set_attr(td_pinch=10)

nw.solve("design")
nw.print_results()
