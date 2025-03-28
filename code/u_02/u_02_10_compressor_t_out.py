'''
simple compressor calculation for
adiabatic compression of air as a real gas
iterative calculation of pressure ratio for 
outlet temperature, compressor efficiency and inlet conditions
belongs to 
unit 2: single components
'''

# use CoolProp
from CoolProp.CoolProp import PropsSI as props

# fluid information
fluid = 'air'

# inlet conditions
m_1 = 10 # mass flow in kg/s
p_1 = 1 * 10**5 # inlet pressure in Pa
t_1 = 293.15 #inlet temperature in K

# compressor data
eta_c = 0.9 # compressor isentropic efficiency
pr_min = 1 # minimum pressure ratio
pr_max = 20 # maximum pressure ratio

# outlet conditions
t_2_target = 573.15 # target compressor outlet tempertature in K


# calculate missing properties
h_1 = props('H', 'P', p_1, 'T', t_1, fluid)
s_1 = props('S', 'P', p_1, 'H', h_1, fluid)

# calculate outlet temperature
def calc_t_out_pr(pr, eta, p_in, h_in, medium):
    '''
    function for calculating outlet temperatures 
    as a function of pressure ratio
    '''
    s_in = props('S', 'P', p_in, 'H', h_in, medium)
    h_out_s = props('H', 'P', p_in*pr, 'S', s_in, medium)
    h_out = h_in + (h_out_s - h_in) / eta
    t_out = props('T', 'P', p_in*pr, 'H', h_out, medium)
    return t_out

t_2_min = calc_t_out_pr(pr_min, eta_c, p_1, h_1, fluid)
t_2_max = calc_t_out_pr(pr_max, eta_c, p_1, h_1, fluid)

print(t_2_min)
print(t_2_target)
print(t_2_max)

# find pressure ratio for target outlet temperature
if (t_2_min < t_2_target) and (t_2_target < t_2_max):
    print('feasible')
    # define search area
    pr_low = pr_min
    pr_high = pr_max
    t_low = t_2_min
    t_high = t_2_max
    pr_found = False
    # bi-sectional search
    while not pr_found:
        print(f'searching, pressure ratio is between {pr_low} and {pr_high}')
        pr_new = (pr_low + pr_high)/2
        t_new = calc_t_out_pr(pr_new, eta_c, p_1, h_1, fluid)
        if t_new > t_2_target:
            pr_high = pr_new
        elif t_new < t_2_target:
            pr_low = pr_new
        else:
            pr_low = pr_new
        pr_found = abs(t_new - t_2_target) < 0.001
else:
    print('out of range')

print('done')
print(pr_new)
