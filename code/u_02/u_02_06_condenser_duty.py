'''
simple model to calculate single sided steam condenser
calculation of duty for 
given in- and outlet conditions
belings to 
unit 2: single components
'''

from CoolProp.CoolProp import PropsSI as prop

# fluid information
fluid = 'water'

# inlet conditions
m_1 = 10 # mass flow in kg/s
p_1 = 1 * 10**5 # pressure in Pa
x_1 = 0.9 # steam quality

# outlet conditions
x_2 = 0 # steam quality for complete condensation

# calculate missing properties
h_1 = prop('H', 'P', p_1, 'Q', x_1, fluid)
p_2 = p_1
h_2 = prop('H', 'P', p_2, 'Q', x_2, fluid)

# calculate duty
q = m_1 * (h_2 - h_1)

print(q)
