from tespy.components import MovingBoundaryHeatExchanger, Source, Sink, Valve, CycleCloser, Compressor
from tespy.connections import Connection
from tespy.networks import Network


def get_cop(working_fluid):
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

    c1.set_attr(fluid={working_fluid: 1}, m=1)
    c2.set_attr(T=15, x=1)

    c4.set_attr(T=60, x=0)

    ev.set_attr(pr1=1, pr2=1)
    cp.set_attr(eta_s=0.85)
    cd.set_attr(pr1=1, pr2=1)

    c11.set_attr(fluid={"water": 1}, T=35, p=1)
    c12.set_attr(T=50)

    c21.set_attr(fluid={"air": 1}, T=20, p=1)
    c22.set_attr(T=15)

    nw.solve("design")

    # we still perform solving in two steps, the first run is to generate
    # a good guess as starting values for pressure and enthalpy in the working
    # fluid cycle, this second run is to ensure no pinch is violated
    ev.set_attr(td_pinch=5)
    c2.set_attr(T=None)
    cd.set_attr(td_pinch=5)
    c4.set_attr(T=None)

    nw.solve("design")

    return abs(cd.Q.val) / cp.P.val


wf_list = ["R290", "NH3", "R134a", "n-Pentane", "R1234ze(Z)", "R1234ze(E)"]

cop = []
for wf in wf_list:
    cop += [get_cop(wf)]


from matplotlib import pyplot as plt

fig, ax = plt.subplots(1)

ax.bar(wf_list, cop)
ax.set_ylabel("COP of the heat pump")

plt.tight_layout()
plt.show()