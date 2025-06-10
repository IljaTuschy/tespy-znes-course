'''
script to simulate a
extraction turbine chp 
with two-sided heating condenser in
design mode
belongs to 
unit 08: Cycles III - CHP
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
    Splitter,
    Merge,
    Valve,
    CycleCloser
)

#create network
chp = Network(p_unit='bar', T_unit='C')

#create components
steg = SimpleHeatExchanger('steam generator')
hptb = Turbine('high pressure turbine')
lptb = Turbine('low pressure turbine')
cond = Condenser('condenser')
pump = Pump('feed water pump')
spli = Splitter('extraction', num_out=2)
heco = Condenser('heating condenser')
valv = Valve('return valve')
merg = Merge('condenser merge', num_in=2)
cc = CycleCloser('cycle closer')

cw_i = Source('cooling water inlet')
cw_o = Sink('cooling water outlet')

dh_r = Source('district heating return')
dh_f = Sink('dirtrict heating supply')

#define topology
c01 = Connection(cc, 'out1', hptb, 'in1', 'c01')
c02 = Connection(lptb, 'out1', merg, 'in1', 'c02')
c03 = Connection(cond, 'out1', pump, 'in1', 'c03')
c04 = Connection(pump, 'out1', steg, 'in1', 'c04')
c00 = Connection(steg, 'out1', cc, 'in1', 'c00')

csi = Connection(hptb, 'out1', spli, 'in1', 'cs1')
cso = Connection(spli, 'out1', lptb, 'in1', 'cs2')

c11 = Connection(spli, 'out2', heco, 'in1', 'c11')
c12 = Connection(heco, 'out1', valv, 'in1', 'c12')
c13 = Connection(valv, 'out1', merg, 'in2', 'c13')

ccm = Connection(merg, 'out1', cond, 'in1', 'ccm')

a01 = Connection(cw_i, 'out1', cond, 'in2', 'a01')
a02 = Connection(cond, 'out2', cw_o, 'in1', 'a02')

d01 = Connection(dh_r, 'out1', heco, 'in2', 'd01')
d02 = Connection(heco, 'out2', dh_f, 'in1', 'd02')

chp.add_conns(c01, c02, c03, c04, c00, csi, cso, ccm, c11, c12, c13, a01, a02, d01, d02)

#define bus
el_net = Bus('generator')
el_net.add_comps({'comp': hptb, 'char': 0.97, 'base': 'component'},
                 {'comp': lptb, 'char': 0.97, 'base': 'component'},
                 {'comp': pump, 'char': 0.97, 'base': 'bus'})

chp.add_busses(el_net)

#set parameters
c01.set_attr(fluid={'water': 1}, T=500, p=100)
a01.set_attr(fluid={'water': 1}, p=1, T=20)
c02.set_attr(p=0.1)

d01.set_attr(fluid={'water':1}, p=10, T=60)
d02.set_attr(T=90)

hptb.set_attr(eta_s=0.9)
lptb.set_attr(eta_s=0.9)
pump.set_attr(eta_s=0.9)
steg.set_attr(pr=0.9)
cond.set_attr(pr1=1, pr2=0.9, ttd_u=5)

heco.set_attr(pr1=1, pr2=0.95, ttd_u=5, Q=-50e6)

el_net.set_attr(P=-50e6)

#simulate design
chp.solve(mode='design')
chp.print_results()
chp.save('code/u_08/chp_results.json')

print(el_net.P.val)
print(heco.get_attr('Q').val)

#store mass flows
m_ls = c01.get_attr('m').val
m_cw = a01.get_attr('m').val
m_dh = d01.get_attr('m').val

#switch to off-design

#turbines (no offdesgin eta char)
hptb.set_attr(offdesign=['cone'])
c01.set_attr(design=['p'])
lptb.set_attr(offdesign=['cone'])
d02.set_attr(design=['T'])
#switch on or off toggling comments to use eta_s_char
hptb.set_attr(design=['eta_s'], offdesign=['eta_s_char', 'cone'])
lptb.set_attr(design=['eta_s'], offdesign=['eta_s_char', 'cone'])


#condensers
cond.set_attr(offdesign=['kA'], design=['ttd_u'])
heco.set_attr(offdesign=['kA'], design=['ttd_u'])

#operating point
a01.set_attr(m=m_cw)
c02.set_attr(design=['p'])
d01.set_attr(m=m_dh)
heco.set_attr(Q=None)
c01.set_attr(m=m_ls)
el_net.set_attr(P=None)

#simulate offdesign
chp.solve(mode='offdesign', design_path='code/u_08/chp_results.json')

chp.print_results()
