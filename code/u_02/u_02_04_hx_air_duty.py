'''
simple heat exchanger calculation for
single sided HX to heat up air as a real gas
straight forward calculation of duty for 
given in- and outlet conditions
belongs to 
unit 2: single components
'''
# properties will be calculated using CoolProp
from CoolProp.CoolProp import PropsSI as prop

# fluid information
fluid = 'air'

# inlet conditions
m_1 = 10 # mass flow in kg/s
t_1 = 293.15 # temperature in K
p_1 = 1 * 10**5 # pressure in Pa

# outlet conditions
t_2 = 393.15 # temperature in K

# clalculate missing properties
h_1 = prop('H', 'P', p_1, 'T', t_1, fluid)
p_2 = p_1
h_2 = prop('H', 'P', p_2, 'T', t_2, fluid)

# claculate duty in W
q = m_1 * (h_2 - h_1)

print(q)
