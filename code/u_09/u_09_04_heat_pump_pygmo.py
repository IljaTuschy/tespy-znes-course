
from tespy.components import Source, Sink, MovingBoundaryHeatExchanger, Compressor, Valve, CycleCloser, SimpleHeatExchanger
from tespy.connections import Connection
from tespy.networks import Network
import numpy as np
import pygmo as pg


class HeatPump:

    def __init__(self):
        self._create_network()

    def _create_network(self):

        nw = Network(T_unit="C", p_unit="bar")

        so_air = Source("air inlet")
        si_air = Sink("air outlet")

        so_water = Source("water inlet")
        si_water = Sink("steam outlet")

        cc_low = CycleCloser("cc lower cycle")
        compressor_low = Compressor("compressor lower cycle")
        internal_heat_exchanger = MovingBoundaryHeatExchanger("internal heat exchanger")
        valve_low = Valve("valve lower cycle")
        evaporator = MovingBoundaryHeatExchanger("evaporator")

        compressor_high = Compressor("compressor higher cycle")
        condenser = MovingBoundaryHeatExchanger("condenser")
        valve_high = Valve("valve higher cycle")
        cc_high = CycleCloser("cc higher cycle")

        a1 = Connection(so_air, "out1", evaporator, "in1", label="a1")
        a2 = Connection(evaporator, "out1", si_air, "in1", label="a2")

        b1 = Connection(cc_low, "out1", compressor_low, "in1", label="b1")
        b2 = Connection(compressor_low, "out1", internal_heat_exchanger, "in1", label="b2")
        b3 = Connection(internal_heat_exchanger, "out1", valve_low, "in1", label="b3")
        b4 = Connection(valve_low, "out1", evaporator, "in2", label="b4")
        b0 = Connection(evaporator, "out2", cc_low, "in1", label="b0")

        c1 = Connection(cc_high, "out1", compressor_high, "in1", label="c1")
        c2 = Connection(compressor_high, "out1", condenser, "in1", label="c2")
        c3 = Connection(condenser, "out1", valve_high, "in1", label="c3")
        c4 = Connection(valve_high, "out1", internal_heat_exchanger, "in2", label="c4")
        c0 = Connection(internal_heat_exchanger, "out2", cc_high, "in1", label="c0")

        d1 = Connection(so_water, "out1", condenser, "in2", label="d1")
        d2 = Connection(condenser, "out2", si_water, "in1", label="d2")

        nw.add_conns(a1, a2, b0, b1, b2, b3, b4, c0, c1, c2, c3, c4, d1, d2)

        a1.set_attr(fluid={"air": 1}, p=1, T=20, m=10)
        a2.set_attr(T=10)

        b1.set_attr(fluid={"R245FA": 1}, x=1, T=0)
        b3.set_attr(x=0, T=60)

        c1.set_attr(fluid={"R1233zd(E)": 1}, x=1, T=55)
        c3.set_attr(T=120, x=0)

        d1.set_attr(fluid={"water": 1}, x=0, T=110)
        d2.set_attr(x=1)

        evaporator.set_attr(pr1=1, pr2=1)
        compressor_low.set_attr(eta_s=0.80)

        internal_heat_exchanger.set_attr(pr1=1, pr2=1)
        compressor_high.set_attr(eta_s=0.8)
        condenser.set_attr(pr1=1, pr2=1)

        nw.solve("design")

        b1.set_attr(T=None)
        evaporator.set_attr(td_pinch=10)

        c1.set_attr(T=None)
        internal_heat_exchanger.set_attr(td_pinch=10)

        c3.set_attr(T=None)
        condenser.set_attr(td_pinch=10)

        nw.solve("design")
        self.nw = nw

    def get_param(self, obj, label, parameter):
        """Get the value of a parameter in the network"s unit system.

        Parameters
        ----------
        obj : str
            Object to get parameter for (Components/Connections).

        label : str
            Label of the object in the TESPy model.

        parameter : str
            Name of the parameter of the object.

        Returns
        -------
        value : float
            Value of the parameter.
        """
        if obj == "Components":
            return self.nw.get_comp(label).get_attr(parameter).val
        elif obj == "Connections":
            return self.nw.get_conn(label).get_attr(parameter).val

    def set_params(self, **kwargs):

        if "Connections" in kwargs:
            for c, params in kwargs["Connections"].items():
                self.nw.get_conn(c).set_attr(**params)

        if "Components" in kwargs:
            for c, params in kwargs["Components"].items():
                self.nw.get_comp(c).set_attr(**params)

    def solve_model(self, **kwargs):
        """
        Solve the TESPy model given the the input parameters
        """
        self.set_params(**kwargs)

        self.solved = False
        try:
            self.nw.solve("design")
            if not self.nw.converged:
                self.nw.solve("design", init_only=True, init_path=self.stable)
            else:
                # might need more checks here!
                if (
                        any(self.nw.results["MovingBoundaryHeatExchanger"]["Q"] > 0)
                        or any(self.nw.results["MovingBoundaryHeatExchanger"]["td_pinch"] < 0)
                    ):
                    self.solved = False
                else:
                    self.solved = True
        except ValueError as e:
            self.nw.lin_dep = True
            self.nw.solve("design", init_only=True, init_path=self.stable)

    def get_objectives(self, objective_list):
        """Get the objective values

        Parameters
        ----------
        objective_list : list
            Names of the objectives

        Returns
        -------
        list
            Values of the objectives
        """
        return [self.get_objective(obj) for obj in objective_list]

    def get_objective(self, objective=None):
        """
        Get the current objective function evaluation.

        Parameters
        ----------
        objective : str
            Name of the objective function.

        Returns
        -------
        objective_value : float
            Evaluation of the objective function.
        """
        if self.solved:
            if objective == "cop":
                condenser, compressor_low, compressor_high = self.nw.get_comp(
                    ["condenser", "compressor lower cycle", "compressor higher cycle"]
                )
                cop = abs(condenser.Q.val) / (compressor_low.P.val + compressor_high.P.val)
                return 1 / cop
            else:
                msg = f"Objective {objective} not implemented."
                raise NotImplementedError(msg)
        else:
            return np.nan


from tespy.tools import OptimizationProblem


plant = HeatPump()

variables = {
    "Connections": {
        "b3": {"T": {"min": 40, "max": 80}}
    }
}

optimize = OptimizationProblem(
    plant, variables, objective=["cop"]
)

num_ind = 5
num_gen = 2

# for algorithm selection and parametrization please consider the pygmo
# documentation! The number of generations indicated in the algorithm is
# the number of evolutions we undertake within each generation defined in
# num_gen
algo = pg.algorithm(pg.ihs(gen=3, seed=42))
# create starting population
pop = pg.population(pg.problem(optimize), size=num_ind, seed=42)

optimize.run(algo, pop, num_ind, num_gen)
print(optimize.individuals)
