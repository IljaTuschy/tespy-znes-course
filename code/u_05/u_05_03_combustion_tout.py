'''
calculation of combustion using tespy
utilization of diabatic combustion chamber 
with given
inlet air condition and mass
fuel condition and outlet temperature
belongs to
unit 5: Cycles I (gas turbines) 
'''

from tespy.networks import Network
from tespy.components import(
    Source,
    DiabaticCombustionChamber,
    Sink
)
from tespy.connections import Connection

#set up network
c = Network()

#define components w/o parametrization
amb = Source('ambient')
tank = Source('tank')
cc = DiabaticCombustionChamber('combustor')
st = Sink('stack')

#define connections
c_air = Connection(amb, 'out1', cc, 'in1', 'combustion air')
c_fuel = Connection(tank, 'out1', cc, 'in2', 'fuel gas')
c_ex = Connection(cc, 'out1', st, 'in1', 'exhaust gas')

c.add_conns(c_air, c_fuel, c_ex)

#parametrization
cc.set_attr(pr=0.95, eta=1)

air = {'O2': 0.21, 'N2': 0.79}
fuel = {'H2': 1}

p_amb = 1e5 #ambient pressure
T_amb = 293.15 #ambient temperature

c_air.set_attr(p=p_amb, T=T_amb, m=100, fluid=air)
c_fuel.set_attr(p=p_amb, T=T_amb, fluid=fuel)

c_ex.set_attr(T=1273.15)

c.solve(mode='design')
c.print_results()
