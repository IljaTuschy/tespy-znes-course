'''
simple heat exchanger calculation for
single sided HX to heat up air as an real gas
straight forward calculation of outlet temperature for 
given mass flow, duty and inlet conditions
belongs to 
unit 2: single components
'''
# use CoolProp for property calculations
from CoolProp.CoolProp import PropsSI as prop

# fluid information
fluid = 'air'

# inlet conditions
m_1 = 10 # mass flow in kg/s
t_1 = 293.15 # temperature in K
p_1 = 1 * 10**5 # pressure in Pa

# HX duty
q = 1000000 # heat exchanger duty in W

# calculate missiong conditions
h_1 = prop('H', 'P', p_1, 'T', t_1, fluid)
p_2 = p_1

# calculate outlet temperature in K 
h_2 = h_1 + q / m_1 

t_2 = prop('T', 'P', p_2, 'H', h_2, fluid)

print(t_2)
