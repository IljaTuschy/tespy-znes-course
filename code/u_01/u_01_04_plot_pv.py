"""
module for starting with python in thermal engineering
plot p,v chart for air
unit 1: calculation of thermal properties
"""
import matplotlib.pyplot as plt
import numpy as np

def calc_v(p, t, r):
    """
    function to calclate volume of ideal gas in m^3/kg using
    p: pressure in Pa
    t: temperature in K
    r: gas constant in J/(kgK)
    """
    return r * t / p

r_out = 287.15 #gas constant in J/(kgK)

#Range for pressures in Pa
p_min = 0.01 * 10**5
p_max = 2.5 * 10**5
p_n = 1000

#Range for temperatures in K
t_min = 100
t_max = 1000
t_n = 10

#Create two arrays holding a set of pressures and temperatures respectively
p_range = np.linspace(p_min, p_max, num=p_n)
t_range = np.linspace(t_min, t_max, num=t_n)

#create array of arrays, holding the calculated volumes
v_range = [calc_v(p_range, t_r, r_out) for t_r in t_range]

#Plotting

#Create a figure that will hold the plots
plt.figure(figsize=[9,6])

#Plot all calculated volumes for each temperature   
for v_t in v_range:
    plt.plot(v_t, p_range)

#Format axes
plt.xlabel('Volume in $\mathrm{m}^3$')
plt.ylabel('Pressure in Pa')
plt.axis([0, 10, 0, p_max])

#Add legend and grid
t_label = [f"T = {T} K" for T in t_range]
plt.legend(t_label)
plt.grid(True)

#Display plot
plt.show()

#Alternatively save plot to file
#plt.savefig("docs/img/pv_air.png")
