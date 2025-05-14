from fluprodia import FluidPropertyDiagram
import matplotlib.pyplot as plt


diagram = FluidPropertyDiagram("Isopentane")


diagram.set_isolines_subcritical(273.15, 500)
diagram.calc_isolines()

fig, ax = plt.subplots(1)

diagram.draw_isolines(fig, ax, "Ts", 0, 1750, 273, 500)

plt.show()
