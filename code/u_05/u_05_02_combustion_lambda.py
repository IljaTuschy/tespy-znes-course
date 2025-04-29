'''
calculation of combustion using tespy
utilization of diabatic combustion chamber 
with given
inlet air condition and mass
fuel condition and lambda
belongs to
unit 5: Cycles I (gas turbines) 
'''

from tespy.networks import Network
from tespy.components import (
    Source,
    DiabaticCombustionChamber,
    Sink
)
from tespy.connections import Connection

#create network
c = Network()

#components w/o any parametrization
amb = Source('ambient')
tank = Source('tank')
cc = DiabaticCombustionChamber('combustion')
st = Sink('stack')

#connections to define topology
c_air = Connection(amb, 'out1', cc, 'in1', 'combustion air')
c_fuel = Connection(tank, 'out1', cc, 'in2', 'fuel gas')
c_ex =Connection(cc, 'out1', st, 'in1', 'exhaust gas')

c.add_conns(c_air, c_fuel, c_ex)

#configuration definig performance, gases and inlet states

#adiabatic combustion chamber with 5% pressure loss
cc.set_attr(eta=1, pr=0.95)

air = {'O2': 0.21, 'N2': 0.79}
fuel = {'H2': 1}

p_amb = 1e5 #ambient pressure
T_amb = 293.15 #ambient temperature
#define air or fuel mass flow
c_air.set_attr(p=p_amb, T=T_amb, fluid=air, m=100)
c_fuel.set_attr(p=p_amb, T=T_amb, fluid=fuel)

#set combustion air to stoichiometric air ratio
cc.set_attr(lamb=1)

#solve and print
c.solve(mode='design')
c.print_results()
