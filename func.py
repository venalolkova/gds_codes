import numpy as np
from math import pi
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts.resonator import RingResonator
from gdshelpers.parts.interferometer import MachZehnderInterferometerMMI
from gdshelpers.layout import GridLayout
from gdshelpers.geometry.ebl_frame_generators import raith_marker_frame


class CrossingConverterTesting:
    def __init__(self):
        self.coupler_params = {
            'width': 1.3,
            'full_opening_angle': np.deg2rad(40),
            'grating_period': 1.155,
            'grating_ff': 0.85,
            'n_gratings': 20,
            'taper_length': 16.
        }

    def inout(self, length, distance, bending_radius, origin=[0, 0], name = None):
        '''
        :param origin: list of [x, y, angle], origin of the first grating, default is [0, 0, 0]
        :param length: float, length of the segment going right after grating coupler (in um)
        :param distance: float, distance between gratings (in um)
        :param bending_radius: float, the bending radius used for the structure (in um)
        :return: list of geometrical objects with test structure of in/out losses
        '''
        if name is None:
            na = 'my cell'
        length1 = length
        length2 = distance - 2 * bending_radius
        coupler_left = GratingCoupler.make_traditional_coupler(origin=origin, **self.coupler_params)
        wg = Waveguide.make_at_port(coupler_left.port)
        wg.add_straight_segment(length1)
        wg.add_bend(-pi / 2, bending_radius)
        wg.add_straight_segment(length2)
        wg.add_bend(-pi / 2, bending_radius)
        wg.add_straight_segment(length1)
        coupler_right = GratingCoupler.make_traditional_coupler_at_port(wg.port, **self.coupler_params)

        cell = Cell('my cell')
        cell.add_to_layer(1, coupler_left, wg, coupler_right)

        return cell

    def bends_array(self, bending_radius, N_bends, distance = None, origin=None, name = None):
        '''
        :param origin: list of [x, y, angle], origin of the first grating, default is [0, 0, 0]
        :param bending_radius: float, bending radius to be tested (in um)
        :param N_bends: number of bends (minimum is 2, then 4*n+2 where n is integer)
        :distance: float, distance between gratings (in um, not less than 4 radii), default is 4*bending_radius
        :return: list of geometrical objects with test structure of bends_array
        '''
        if origin is None:
            origin = [0, 0]
        if distance is None:
            distance = 4*bending_radius
        if name is None:
            na = 'my cell'
        l = distance - 4 * bending_radius
        coupler_left = GratingCoupler.make_traditional_coupler(origin=origin, **self.coupler_params)
        wg = Waveguide.make_at_port(coupler_left.port)
        wg.add_bend(-pi / 2, bending_radius)
        n = (N_bends - 6) / 2
        while n > 0:
            wg.add_bend(pi, bending_radius)
            wg.add_bend(-pi, bending_radius)
            n -= 4
        wg.add_bend(pi / 2, bending_radius)
        wg.add_bend(-pi / 2, bending_radius)
        wg.add_straight_segment(l)
        wg.add_bend(-pi / 2, bending_radius)
        wg.add_bend(pi / 2, bending_radius)
        n = (N_bends - 6) / 2
        while n > 0:
            wg.add_bend(-pi, bending_radius)
            wg.add_bend(pi, bending_radius)
            n -= 4
        wg.add_bend(-pi / 2, bending_radius)

        coupler_right = GratingCoupler.make_traditional_coupler_at_port(wg.port, **self.coupler_params)

        cell = Cell(name)
        cell.add_to_layer(1, coupler_left, wg, coupler_right)

        return cell
