from CoolProp.CoolProp import PropsSI as PSI
import numpy as np
from matplotlib import pyplot as plt


fluids = ["water", "Isopentane", "cyclopentane", "n-Pentane", "n-Butane", "Isobutane"]
fig, ax = plt.subplots(1)

for i, fluid in enumerate(fluids):

    dome_T = np.linspace(273.15, PSI("Tcrit", fluid))
    dome_Q_0_s = PSI("S", "T", dome_T, "Q", 0, fluid)
    dome_Q_1_s = PSI("S", "T", dome_T, "Q", 1, fluid)

    _ = ax.plot(dome_Q_0_s, dome_T - 273.15)
    ax.plot(dome_Q_1_s, dome_T - 273.15, color=_[0].get_color(), label=fluid)

ax.set_xlabel("entropy in J/kgK")
ax.set_ylabel("temperature in °C")
ax.legend()

plt.tight_layout()
plt.show()
