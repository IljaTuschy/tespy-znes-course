'''
simple compressor calculation for
adiabatic compression of air as a real gas
straight forward calculation of duty for given 
compressor data and inlet conditions
belongs to 
unit 2: single components
'''

# use CoopProp for property calculation
from CoolProp.CoolProp import PropsSI as prop

# fluid information
fluid = 'air'

# inlet properties
m_1 = 10 # mass flow in kg/s
p_1 = 1 * 10**5 # pressure in Pa
t_1 = 293.15 # temperature in K

# compressor data
pr = 10 # pressure ratio
eta_c = 0.9 # isentropic efficiency

# calculate missing properties
h_1 = prop('H', 'P', p_1, 'T', t_1, fluid)

# make use of component data
p_2 = p_1 * pr
s_1 = prop('S', 'P', p_1, 'H', h_1, fluid)
h_2s = prop('H', 'P', p_2, 'S', s_1, fluid)
h_2 = h_1 + (h_2s - h_1) / eta_c

# calculate compressor duty
power = m_1 * (h_2 - h_1)

print(power)
