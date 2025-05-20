from tespy.components import Source, Sink, Compressor
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

so = Source("source")
si = Sink("sink")
compressor = Compressor("compressor")

c1 = Connection(so, "out1", compressor, "in1", label="c1")
c2 = Connection(compressor, "out1", si, "in1", label="c2")

nw.add_conns(c1, c2)

c1.set_attr(fluid={"air": 1}, m=1, p=1, T=25)
c2.set_attr(p=10)

compressor.set_attr(eta_s=0.85)

nw.solve("design")
nw.print_results()
nw.save("compressor_design.json")

compressor.set_attr(
    design=["eta_s"], offdesign=["char_map_eta_s", "char_map_pr"],
    # these equations only work in connection with a inlet guide vane angle
    # 0 is the neutral position
    igva=0
)
c2.set_attr(design=["p"])

nw.solve("offdesign", design_path="compressor_design.json")
nw.print_results()


import numpy as np


# the compressor maps are really tight per speedline
m_range = np.linspace(0.948, 1.006)
eta_s_range = []
pr_range = []

for m in m_range:
    c1.set_attr(m=m)
    nw.solve("offdesign", design_path="compressor_design.json")
    eta_s_range.append(compressor.eta_s.val)
    pr_range.append(compressor.pr.val)


import matplotlib.pyplot as plt


fig, ax = plt.subplots(2)

ax[0].scatter(m_range, pr_range)
ax[1].scatter(m_range, eta_s_range)

ax[0].set_ylabel("Pressure ratio of compressor")
ax[1].set_ylabel("Isentopic efficiency")
ax[0].set_xlabel("Mass flow in kg/s")

plt.tight_layout()
plt.show()

# we can shift the speedlines with the igva
m_range = np.linspace(0.5, 1.1)
eta_s_range = []
igva_range = []

compressor.set_attr(igva=None)
compressor.set_attr(igva="var", pr=10)

# unfortunately the results are extremely senstive to change in ivga
# we have to make tiny steps here, and even that does not completely help
# outlet enthalpy equation does not converge
nw.set_attr(iterinfo=False)
m_range = np.linspace(0.25, 1.01, 200)
for m in m_range:
    c1.set_attr(m=m)
    nw.solve("offdesign", design_path="compressor_design.json")
    eta_s_range.append(compressor.eta_s.val)
    igva_range.append(compressor.igva.val)


import matplotlib.pyplot as plt


fig, ax = plt.subplots(2)

ax[0].scatter(m_range, igva_range)
ax[1].scatter(m_range, eta_s_range)

ax[0].set_ylabel("Inlet guide vane angle in °")
ax[1].set_ylabel("Isentopic efficiency")
ax[0].set_xlabel("Mass flow in kg/s")

plt.tight_layout()
plt.show()
