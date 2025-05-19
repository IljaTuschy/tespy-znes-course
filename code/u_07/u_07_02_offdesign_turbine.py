'''
script to simulate off-design opreration of a 
steam turbine

with a default efficiency characteristic

belongs to 

Unit 07: Design and Off-Design

'''

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import(
    Source,
    Turbine,
    Sink
)

#create network
tn = Network()

#create components
ls = Source('life steam')
turb = Turbine('steam turbine')
ex = Sink('turbine exhaust')

#set up topology
c01 = Connection(ls, 'out1', turb, 'in1', 'c01')
c02 = Connection(turb, 'out1', ex, 'in1', 'c02')

tn.add_conns(c01, c02)

#parametrize

#given in exersise
fluid = {'water': 1}
T_ls = 550+273.15 #inlet temperature in K
p_ls = 80e5 #inlet pressure in Pa
p_ex = 0.1e5 #turbine outlet pressure in Pa

#additionally needed for design
m = 100 #mass flow in kg/s
eta = 0.85 #isentropic turbine efficiency

c01.set_attr(fluid=fluid, p=p_ls, T=T_ls, m=m)
c02.set_attr(p=p_ex)
turb.set_attr(eta_s=eta)

#design calculation
tn.solve(mode='design')
tn.print_results()
tn.save('turbine_results.json')

#calculate off design for identical mass flow
turb.set_attr(design=['eta_s'], offdesign=['eta_s_char', 'cone'])
c01.set_attr(p=None)
tn.solve(mode='offdesign', design_path='turbine_results.json')
tn.print_results()

#calculate off design for other mass flow
c01.set_attr(m=m*0.5)
tn.solve(mode='offdesign', design_path='turbine_results.json')
tn.print_results()
