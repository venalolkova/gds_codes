import numpy as np
from math import pi
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts.resonator import RingResonator
from gdshelpers.parts.interferometer import MachZehnderInterferometerMMI
from gdshelpers.layout import GridLayout
from gdshelpers.geometry.ebl_frame_generators import raith_marker_frame

coupler_params = {
    'width': 1.3,
    'full_opening_angle': np.deg2rad(40),
    'grating_period': 1.155,
    'grating_ff': 0.85,
    'n_gratings': 20,
    'taper_length': 16.
}
def inout(length, bending_radius):
    coupler_left=GratingCoupler.make_traditional_coupler(origin=[0, 0], **coupler_params)
    wg1 = Waveguide.make_at_port(coupler_left.port)
    wg1.add_straight_segment(10)
    wg1.add_bend(-pi/2, 40)
def AMZI(difference, length, name):
    coupler_left=GratingCoupler.make_traditional_coupler(origin=[0, 0], **coupler_params)
    wg1 = Waveguide.make_at_port(coupler_left.port)
    wg1.add_straight_segment(10)
    wg1.add_bend(-pi/2, 40)
    mmi = MachZehnderInterferometerMMI.make_at_port(wg1.port, 10, 4, 5,
                                                    10, 20, 120)
    wg2 = Waveguide.make_at_port(mmi.port)
    wg2.add_bend(-pi/2, 40)
    wg1.add_straight_segment(10)
    coupler_right=GratingCoupler.make_traditional_coupler_at_port(wg2.current_port, **coupler_params)
    cell = Cell(name)
    cell.add_to_layer(1, coupler_left, wg1, mmi, wg2, coupler_right)

    return cell


row_nums = np.arange(1, 6, 1)
column_nums = np.arange(1, 6, 1)
layout = GridLayout('ANZI array', frame_layer=0, text_layer=2, region_layer_type=None)
layout.add_column_label_row(('Row %0.1f' % row for row in row_nums), row_label='')
for column in column_nums:
    layout.begin_new_row(f'{column}')
    for row in row_nums:
        layout.add_to_row(AMZI(1, 2, f'{row, column}'))

layout_cell, mapping = layout.generate_layout()
layout_cell.add_frame(frame_layer=8, line_width=5)
layout_cell.add_ebl_frame(layer=10, frame_generator=raith_marker_frame, n=2)
layout_cell.show()
layout_cell.save('interferometers.gds')