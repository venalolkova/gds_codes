import numpy as np
from math import pi
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts.text import Text
from func import *
from gdshelpers.helpers import id_to_alphanumeric

structure = CrossingConverterTesting()
io = structure.inout(10, 150, 10, name='in_out')
ba1 = structure.bends_array(10, 52, name='52 bends')
ba2 = structure.bends_array(10, 100, name='100 bends')
dl1 = structure.delay_line(10000, 10, 100, name='10 cm delay line')
dl2 = structure.delay_line(15000, 10, 100, name='15 cm delay line')
amzi = structure.amzi(10, 'amzi1')
amzi_chiplet = structure.amzi_converter(10, 'amzi+chiplet')

cell_main = Cell("testchip_big")


cell_id = id_to_alphanumeric(0, 0)
cell = Cell(cell_id)
cell.add_cell(io)
cell.add_to_layer(1, Text([-30, -70], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(0, 0))

cell_id = id_to_alphanumeric(1, 0)
cell = Cell(cell_id)
cell.add_cell(ba1)
cell.add_to_layer(1, Text([-30, -70], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(200, 0))

cell_id = id_to_alphanumeric(2, 0)
cell = Cell(cell_id)
cell.add_cell(ba2)
cell.add_to_layer(1, Text([-30, -70], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(350, 0))

cell_id = id_to_alphanumeric(3, 0)
cell = Cell(cell_id)
cell.add_cell(dl1)
cell.add_to_layer(1, Text([-100, -100], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(550, 0))

cell_id = id_to_alphanumeric(4, 0)
cell = Cell(cell_id)
cell.add_cell(dl2)
cell.add_to_layer(1, Text([-100, -100], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(750, 0))

cell_id = id_to_alphanumeric(0, 1)
cell = Cell(cell_id)
cell.add_cell(amzi)
cell.add_to_layer(1, Text([-100, -100], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(0, -200))

cell_id = id_to_alphanumeric(0, 2)
cell = Cell(cell_id)
cell.add_cell(amzi_chiplet)
cell.add_to_layer(1, Text([-100, -100], 20, f'{cell_id}'))
cell_main.add_cell(cell, origin=(400, -200))

cell_main.save()

