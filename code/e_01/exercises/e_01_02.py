'''
script to calculate the gross efficiency 
of a steam power plant process with a 
single feedwater preheater
'''
from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    SimpleHeatExchanger,
    Turbine,
    Splitter,
    Pump,
    Condenser,
    Valve,
    Merge,
    CycleCloser
)

# create network
plant = Network(T_unit='C', p_unit='bar')

# create components w/o parametrization
stg = SimpleHeatExchanger('steam generator')
hpt = Turbine('high pressure turbine')
ext = Splitter('turbine extraction')
lpt = Turbine('low pressure turbine')
ret = Merge('heating condensate return')
con = SimpleHeatExchanger('main condenser')
fwp = Pump('feed water pump')
fwh = Condenser('feed water preheater')
val = Valve('return valve')
cc = CycleCloser('cycle closer')

# define topology w/o parametrization
c00 = Connection(stg, 'out1', cc, 'in1', 'c00')
c01 = Connection(cc, 'out1', hpt, 'in1', 'c01')
c02 = Connection(hpt, 'out1', ext, 'in1', 'c02')
c03 = Connection(ext, 'out1', lpt, 'in1', 'c03')
c04 = Connection(lpt, 'out1', ret, 'in1', 'c04')
c05 = Connection(ret, 'out1', con, 'in1', 'c05')
c06 = Connection(con, 'out1', fwp, 'in1', 'c06')
c07 = Connection(fwp, 'out1', fwh, 'in2', 'c07')
c08 = Connection(fwh, 'out2', stg, 'in1', 'c08')
c09 = Connection(ext, 'out2', fwh, 'in1', 'c09')
c10 = Connection(fwh, 'out1', val, 'in1', 'c10')
c11 = Connection(val, 'out1', ret, 'in2', 'c11')

plant.add_conns(c00, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11)

# parametrize
# components
stg.set_attr(pr=0.8)
hpt.set_attr(eta_s=0.9)
lpt.set_attr(eta_s=0.9)
con.set_attr(pr=1)
fwp.set_attr(eta_s=0.75)
fwh.set_attr(pr1=1, pr2=1)
fwh.set_attr(pr1=1, pr2=1, ttd_u=3)

# connections
c01.set_attr(fluid={'water':1}, T=520, p=80, m=100)
c02.set_attr(p=5)
c04.set_attr(p=0.1)
c06.set_attr(x=0)
# provide starting value for preheater in order to 
# make setup with ttd_u specification work
c08.set_attr(h0=640000)

plant.solve(mode='design')
plant.print_results()

eta = abs(hpt.get_attr('P').val + lpt.get_attr('P').val)/stg.get_attr('Q').val
print(f'The gross cycle efficiency is {eta:0.2%}.')
