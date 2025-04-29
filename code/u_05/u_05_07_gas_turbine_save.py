'''
calculation of gas turbine cycle using tespy
using labda as the most generic and stable 
approach to define the operation of
diabatic combustion chamber 
and then save network
belongs to
unit 5: Cycles I (gas turbines) 
'''
from tespy.networks import Network
from tespy.components import (
    Source,
    Compressor,
    DiabaticCombustionChamber,
    Turbine,
    Sink
)
from tespy.connections import Connection

#define network
gt = Network()

#define components w/o any parameters
amb = Source('ambient')
tank = Source('fuel tank')
comp = Compressor('compressor')
cc = DiabaticCombustionChamber('combustion chamber')
turb = Turbine('turbine')
st = Sink('stack')

#define connections w/o any parameters
ai = Connection(amb, 'out1', comp, 'in1', 'air intake')
co = Connection(comp, 'out1', cc, 'in1', 'compressor outlet')
cf = Connection(tank, 'out1', cc, 'in2', 'combustion fuel')
ti = Connection(cc, 'out1', turb, 'in1', 'turbine inlet')
exh = Connection(turb, 'out1', st, 'in1', 'turbine exhaust')

gt.add_conns(ai, co, cf, ti, exh)

#parametrize problem

#fluids
air = {'N2': 0.79, 'O2': 0.21}
fuel = {'H2': 1}

#ambient conditions
p_amb = 1e5 #pressure in Pa
T_amb = 293.15 #temperature in K

#combustion chamber pressure
p_cc = 12e5

#connection data
ai.set_attr(p=p_amb, T=T_amb, m=100, fluid=air)
co.set_attr(p=p_cc)
cf.set_attr(p=p_cc, T=T_amb, fluid=fuel)
exh.set_attr(p=p_amb)

#component data
comp.set_attr(eta_s=0.9)
cc.set_attr(pr=0.95, eta=1, lamb=12)
turb.set_attr(eta_s=0.9)

gt.solve(mode='design')
gt.print_results()

#print(f'The efficiency is {(abs(turb.P.val) - comp.P.val) / cc.calc_ti():.2%}')

P_turb = turb.get_attr('P').val
P_comp = comp.get_attr('P').val
print(f'The efficiency is {(abs(P_turb) - P_comp) / cc.calc_ti():.2%}')

#save stable relsuts for use in other calculations
gt.save('code/u_05/gt_stable.json')
#for older versions of tespy
#gt.save('code/u_05/gt_stable_results/')
