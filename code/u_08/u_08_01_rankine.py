'''
scipt to clacluate a simple
rankine cycle with 
given output using
bus component
belongs to 
unit 08: Cycles III
'''

from tespy.networks import Network
from tespy.connections import Connection, Bus
from tespy.components import(
    Source,
    Sink,
    SimpleHeatExchanger,
    Turbine,
    Condenser,
    Pump,
    CycleCloser    
)

#create network
pp = Network(p_unit='bar', T_unit='C')

#create components
steg = SimpleHeatExchanger('steam generator')
turb = Turbine('turbine')
cond = Condenser('condenser')
pump = Pump('feed water pump')
cc = CycleCloser('cycle closer')

cw_i = Source('cooling water inlet')
cw_o = Sink('cooling water outlet')

#define topology
c01 = Connection(cc, 'out1', turb, 'in1', 'c01')
c02 = Connection(turb, 'out1', cond, 'in1', 'c02')
c03 = Connection(cond, 'out1', pump, 'in1', 'c03')
c04 = Connection(pump, 'out1', steg, 'in1', 'c04')
c00 = Connection(steg, 'out1', cc, 'in1', 'c00')

a01 = Connection(cw_i, 'out1', cond, 'in2', 'a01')
a02 = Connection(cond, 'out2', cw_o, 'in1', 'a02')

pp.add_conns(c01, c02, c03, c04, c00, a01, a02)

#define bus
el_net = Bus('generator')
el_net.add_comps({'comp': turb, 'char': 0.97, 'base': 'component'},
                 {'comp': pump, 'char': 0.97, 'base': 'bus'})

pp.add_busses(el_net)

#set parameters
c01.set_attr(fluid={'water': 1}, T=500, p=100)
a01.set_attr(fluid={'water': 1}, p=1, T=20)
c02.set_attr(p=0.1)

turb.set_attr(eta_s=0.9)
pump.set_attr(eta_s=0.9)
steg.set_attr(pr=0.9)
cond.set_attr(pr1=1, pr2=0.9, ttd_u=5)

el_net.set_attr(P=-50e6)

#simulate design
pp.solve(mode='design')
pp.print_results()

print(el_net.P.val)
