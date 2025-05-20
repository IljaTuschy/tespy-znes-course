from tespy.components import Source, Sink, Turbine
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

so = Source("source")
si = Sink("sink")
turbine = Turbine("steam turbine")

c1 = Connection(so, "out1", turbine, "in1", label="c1")
c2 = Connection(turbine, "out1", si, "in1", label="c2")

nw.add_conns(c1, c2)

c1.set_attr(fluid={"water": 1}, m=1, p=80, T=550)
c2.set_attr(p=0.1)

turbine.set_attr(eta_s=0.9)

nw.solve("design")
nw.print_results()
nw.save("turbine_design.json")

turbine.set_attr(design=["eta_s"], offdesign=["eta_s_char"])
nw.solve("offdesign", design_path="turbine_design.json")
nw.print_results()

nw.set_attr(iterinfo=False)

import matplotlib.pyplot as plt

import numpy as np

eta_s_range = []
m_range = np.linspace(0.5, 1.2)
for m in m_range:
    c1.set_attr(m=m)
    nw.solve("offdesign", design_path="turbine_design.json")
    eta_s_range.append(turbine.eta_s.val)

eta_s_range = np.array(eta_s_range) * 100

fig, ax = plt.subplots(1)

ax.plot(m_range, eta_s_range)
ax.set_ylabel("Isentropic efficiency in %")
ax.set_xlabel("Turbine mass flow in kg/s")

plt.tight_layout()
plt.show()
