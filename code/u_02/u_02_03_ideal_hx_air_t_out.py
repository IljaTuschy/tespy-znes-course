'''
simple heat exchanger calculation for
single sided HX to heat up air as an ideal gas
straight forward calculation of outlet temperature for 
given mass flow, duty and inlet conditions
belongs to 
unit 2: single components
'''

# ideal gas parameters
c_p = 1100 # specific heat of air in J/(kgK)

# inlet conditions
m_1 = 10 # mass flow in kg/s 
t_1 = 293.15 # temperature in K

# outlet conditions

q = 1000000 # heat exchanger duty in W

# calculate outlet temperature in K 
t_2 = t_1 + q / (m_1 * c_p)

print(t_2)
