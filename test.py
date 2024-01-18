import numpy as np
from math import pi
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts.text import Text
from func import *
from gdshelpers.helpers import id_to_alphanumeric

structure = CrossingConverterTesting()
io = structure.inout(10, 150, 10, name = '1')
ba = structure.bends_array(10, 52, name = '2')

cell_main = Cell("testchip_big")


cell_id = id_to_alphanumeric(0, 1)
cell = Cell(cell_id)
cell.add_cell(io)
cell.add_to_layer(1, Text([-30, 0], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(200, 0))


cell_id = id_to_alphanumeric(1, 1)
cell = Cell(cell_id)
cell.add_cell(ba)
cell.add_to_layer(1, Text([-30, 0], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(400, 0))

cell_main.save()


