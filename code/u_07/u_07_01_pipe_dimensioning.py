from tespy.components import Source, Sink, Pipe
from tespy.connections import Connection
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

so = Source("source")
si = Sink("sink")
pipe = Pipe("pipeline")

c1 = Connection(so, "out1", pipe, "in1", label="c1")
c2 = Connection(pipe, "out1", si, "in1", label="c2")

nw.add_conns(c1, c2)

c1.set_attr(fluid={"Air": 1}, m=1, p=5, T=25)
c2.set_attr(T=25)

pipe.set_attr(dp=0.02, ks=0.00005, L=200, D="var")

nw.solve("design")
nw.print_results()

print(f"Diameter of the pipe: {round(pipe.D.val, 3)} m")

# We can also have a look at the volumetric flows a the inlet and at the outlet
print(f"v_dot inflow: {round(c1.v.val, 3)} m3/s")
print(f"v_dot outflow: {round(c2.v.val, 3)} m3/s")

pipe.set_attr(D=pipe.D.val, dp=None)

nw.solve("design")
nw.print_results()
nw.set_attr(iterinfo=False)

import matplotlib.pyplot as plt

import numpy as np

dp_range = []
m_range = np.linspace(0.5, 10)
for m in m_range:
    c1.set_attr(m=m)
    nw.solve("design")
    dp_range.append(pipe.dp.val)

plt.plot(m_range, dp_range)
plt.show()
