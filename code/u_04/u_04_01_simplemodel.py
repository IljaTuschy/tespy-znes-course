from tespy.components import SimpleHeatExchanger, Source, Sink, Valve, CycleCloser, Compressor
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

ev = SimpleHeatExchanger("evaporator")
cp = Compressor("compressor")
cd = SimpleHeatExchanger("condenser")
va = Valve("valve")
cc = CycleCloser("cycle closer")

c1 = Connection(cc, "out1", ev, "in1", label="1")
c2 = Connection(ev, "out1", cp, "in1", label="2")
c3 = Connection(cp, "out1", cd, "in1", label="3")
c4 = Connection(cd, "out1", va, "in1", label="4")
c0 = Connection(va, "out1", cc, "in1", label="0")

nw.add_conns(c1, c2, c3, c4, c0)

c1.set_attr(fluid={"R290": 1}, m=1)
c2.set_attr(T=15, x=1)

c4.set_attr(T=60, x=0)

ev.set_attr(pr=1)
cp.set_attr(eta_s=0.85)
cd.set_attr(pr=1)

nw.solve("design")
nw.print_results()

# we can access the component properties through the .val attribute of the
# respective property
# NOTE: component data is always returned as SI value
cop = abs(cd.Q.val) / cp.P.val
print(f"COP = {cop}")

# we can collect the states in two lists by iterating over the respective
# connections and accessing .h.val and .p.val
# NOTE: connection data come in the unit specified in the network setup
states_h = [c.h.val for c in [c1, c2, c3, c4, c0]]
states_p = [c.p.val for c in [c1, c2, c3, c4, c0]]

from matplotlib import pyplot as plt

fig, ax = plt.subplots(1)

ax.scatter(states_h, states_p)
ax.plot(states_h, states_p)

ax.set_yscale("log")
ax.set_ylabel("pressure in bar")
ax.set_xlabel("enthalpy in J/kg")

plt.tight_layout()
plt.show()
