'''
module for starting with python in thermal engineering
calculate and plott the compressibility of air using coolprop
belongs to 
unit 1: calculation of thermal properties
'''
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI as prop

p = 10**5
t = 273.15
r_i = 287.

p_range = np.linspace(0.1*10**5, 100*10**5, num=1000)
t_range = np.linspace(200, 400, num=11)

fluid = 'Air'

z_range = [1/prop('D', 'P', p_range, 'T', t_r, fluid) / (r_i * t_r / p_range) for t_r in t_range]

plt.figure()
for z_r in z_range:
    plt.plot(p_range, z_r)
plt.xlabel('Pressure in Pa')
plt.ylabel('$Z=pv/R_iT$')
plt.title('Compressibility of Air')
plt.axis([0, 100*10**5, 0.8, 1.2])
label = [f'T = {t_r} K'for t_r in t_range]
plt.legend(label, loc=9, ncols=3)
plt.grid(True)
plt.show()
