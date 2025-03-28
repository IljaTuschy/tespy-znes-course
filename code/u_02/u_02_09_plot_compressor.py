'''
simple model for plotting compressor performance info
for adiabatic compressors compressing air as a real gas
calculates outlet temperature and duty for
given compressor data and inlet conditions
belongs to 
unit 2: single components
'''

# use CoopProp for properties
from CoolProp.CoolProp import PropsSI as prop 

# use matplotlib for plotting
import matplotlib.pyplot as plt

# use numpy for efficient handling of arrays
import numpy as np


# fluid information
fluid = 'air'

# inlet conditions
m_1 = 10 # mass flow in kg/s
p_1 = 1 * 10 **5 # pressure in Pa
t_1 = 293.15 # temperature in K

# compressor data
pr_min = 1 # minimum pressure ratio
pr_max = 20 # maximum pressure ratio
eta_min = 0.7 # minimum efficiency
eta_max = 0.95 # maximum efficiency

pr_range = np.linspace(pr_min, pr_max, num=200)
eta_range = np.linspace(eta_min, eta_max, num=6)

# calculate maximum outlet temperature
def calc_t2(p_in, h_in, pr, eta, medium):
    '''
    calculates outlet temperature
    '''
    s_in = prop('S', 'P', p_in, 'H', h_in, medium)
    h_out_s = prop('H', 'P', p_in*pr, 'S', s_in, medium)
    h_out = h_in + (h_out_s - h_in) / eta
    return prop('T', 'P', p_in*pr, 'H', h_out, medium)

# calculate missing properties
h_1 = prop('H', 'P', p_1, 'T', t_1, fluid)

# calculate outlet temperature
t_2max = calc_t2(p_1, h_1, pr_max, eta_min, fluid)

t_2 = [calc_t2(p_1, h_1, pr_range, eta_c, fluid) for eta_c in eta_range]

# plot outlet temperatures
fig = plt.figure()
ax = fig.add_subplot(111)
for t in t_2:
    ax.plot(pr_range, t-273.15)
ax.set_ylabel('Outlet Temperature in °C')
ax.set_ylim(t_1-273.15, t_2max-273.15)
ax.set_xlabel('Pressure Ratio')
ax.set_xlim(pr_min, pr_max)
ax.grid(True)
labels = [f'eta = {(eta):2.0%}' for eta in eta_range]
ax.legend(labels)
ax.set_title(f'Air Compressor Performance for {t_1-273.15} °C and {p_1/10**5} bar at inlet' )
plt.show()
