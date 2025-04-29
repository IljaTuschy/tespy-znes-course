from tespy.components import MovingBoundaryHeatExchanger, Source, Sink, Valve, CycleCloser, Compressor
from tespy.connections import Connection
from tespy.networks import Network
from CoolProp.CoolProp import PropsSI


nw = Network(T_unit="C", p_unit="bar")

ev = MovingBoundaryHeatExchanger("evaporator")
cp = Compressor("compressor")
cd = MovingBoundaryHeatExchanger("condenser")
va = Valve("valve")
cc = CycleCloser("cycle closer")

water_cold = Source("Cold water")
water_hot = Sink("Hot water")
air_intake = Source("Air intake")
air_outlet = Sink("Air outlet")

c1 = Connection(cc, "out1", ev, "in2", label="1")
c2 = Connection(ev, "out2", cp, "in1", label="2")
c3 = Connection(cp, "out1", cd, "in1", label="3")
c4 = Connection(cd, "out1", va, "in1", label="4")
c0 = Connection(va, "out1", cc, "in1", label="0")

nw.add_conns(c1, c2, c3, c4, c0)

c11 = Connection(water_cold, "out1", cd, "in2", label="11")
c12 = Connection(cd, "out2", water_hot, "in1", label="12")

c21 = Connection(air_intake, "out1", ev, "in1", label="21")
c22 = Connection(ev, "out1", air_outlet, "in1", label="22")

nw.add_conns(c11, c12, c21, c22)

c1.set_attr(fluid={"R290": 1}, m=1)
c2.set_attr(T=15, x=1)

c4.set_attr(T=60, x=0)

ev.set_attr(pr1=1, pr2=1)
cp.set_attr(eta_s=0.85)
cd.set_attr(pr1=1, pr2=1)

c11.set_attr(fluid={"water": 1}, T=35, p=1)
c12.set_attr(T=50)

c21.set_attr(fluid={"air": 1}, T=20, p=1, m=10)

nw.solve("design")

ev.set_attr(td_pinch=5)
c2.set_attr(T=None)
cd.set_attr(td_pinch=5)
c4.set_attr(T=None)

# We will remove the ambient air specification to find at what air temperature
# the cop is exactly 5. This specification will be replaced by a
# UserDefinedEquation, which directly sets the cop to be equal to 5
c21.set_attr(T=None)

# first we define the equation:
# COP = delta h_condenser / delta h_compressor
# 0 = COP * delta h_compressor - delta h_condenser
# The connections are accessible through the ude.conns attribute
# the cop will be available through ude.params["cop"]
def cop_func(ude):
    c2, c3, c4 = ude.conns
    cop = ude.params["cop"]
    return cop * (c3.h.val_SI - c2.h.val_SI) - (c3.h.val_SI - c4.h.val_SI)

# Next we need to define the partial derivatives
# c2 enthalpy: -cop
# c3 enthalpy: cop - 1
# c4 enthalpy: 1
# no other variables are part of the equation
def cop_deriv(ude):
    c2, c3, c4 = ude.conns
    cop = ude.params["cop"]
    if c2.h.is_var:
        ude.jacobian[c2.h.J_col] = -cop
    if c3.h.is_var:
        ude.jacobian[c3.h.J_col] = cop - 1
    if c4.h.is_var:
        ude.jacobian[c4.h.J_col] = 1

# Then we define the UserDefinedEquation by importing the class and passing
# the respective parameters
from tespy.tools import UserDefinedEquation

cop_ude = UserDefinedEquation(
    "fixed-cop-eq",
    func=cop_func,
    deriv=cop_deriv,
    conns=[c2, c3, c4],
    params={"cop": 4}
)
nw.add_ude(cop_ude)

nw.solve("design")
nw.print_results()

cop_result = abs(cd.Q.val) / cp.P.val
print(f"The resulting cop is: {cop_result}")

# Modification is possible:
cop_ude.params["cop"] = 5

nw.solve("design")

cop_result = abs(cd.Q.val) / cp.P.val
print(f"The resulting cop is: {cop_result}")
