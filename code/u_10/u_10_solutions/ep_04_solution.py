'''
script to determine the vapor content
after a flash process for water
with given boiling temperature
'''

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Source,
    Pump,
    SimpleHeatExchanger,
    Valve,
    Sink
)

# create network and set unit system
nw = Network(p_unit='bar', T_unit='C')

# create components
tank = Source('water tank')
pump = Pump('water pump')
heat = SimpleHeatExchanger('boiler')
valv = Valve('flash valve')
flas = Sink('flash tank')

# set up topology without parametrization
# refer to hbd for connection names
c1 = Connection(tank, 'out1', pump, 'in1', 'c1')
c2 = Connection(pump, 'out1', heat, 'in1', 'c2')
c3 = Connection(heat, 'out1', valv, 'in1', 'c3')
c4 = Connection(valv, 'out1', flas, 'in1', 'c4')

nw.add_conns(c1, c2, c3, c4)

# parametrize
# water tank conditions
# boiling temperature
# flash tank pressure
c1.set_attr(fluid={'water':1}, m=10, p=1, T=20)
c3.set_attr(T=200, x=0)
c4.set_attr(p=1)
# component efficiencies
pump.set_attr(eta_s=0.75)
heat.set_attr(pr=0.95)

# solve and print results
nw.solve(mode='design')
nw.print_results()
res = c4.get_attr('x').val
print(f'The vapor content at the flash tank inlet is {res:.1%}')
