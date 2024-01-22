import numpy as np
from math import pi
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts import Port
from gdshelpers.parts.splitter import MMI
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
            name = 'inout'
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

        cell = Cell(name)
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
            name = 'bends_array'
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
    def delay_line (self, length, bending_radius, grating_distance, name=None):
        dif = 2
        if name is None:
            name = 'delay line'
        d = grating_distance
        L = length
        R = bending_radius
        L_b = pi/2*R
        # coupler_left = GratingCoupler.make_traditional_coupler(origin=origin, **self.coupler_params)

        wg1 = Waveguide.make_at_port(Port([0, 0], 0, 0.5))
        wg2 = Waveguide.make_at_port(Port([0, 0], pi, 0.5))
        wg1.add_bend(pi, R)
        wg1.add_bend(-pi, R)

        L-=2*pi*R
        wg2.add_straight_segment(dif)
        wg2.add_bend(-pi / 2, R)
        wg2.add_straight_segment(2 * R + dif)
        wg2.add_bend(-pi / 2, R)
        L-=(pi+2)*R-2*dif
        i = 1
        while L>=0:
            dif_2 = dif+2*i*dif
            dif_1 = dif + 2 * (i-1) * dif
            wg2.add_straight_segment(dif_2)
            wg2.add_bend(-pi/2, R)
            wg2.add_straight_segment(2*R+dif_2)
            wg2.add_bend(-pi/2, R)

            wg1.add_straight_segment(dif_1)
            wg1.add_bend(-pi/2, R)
            wg1.add_straight_segment(2*R+dif_1)
            wg1.add_bend(-pi/2, R)

            L-=2*dif_2+2*dif_1+pi*2*R+4*R
            i+=1

        wg1.add_straight_segment(d-dif)
        wg1.add_bend(pi/2, R)
        wg2.add_bend(pi / 2, R)

        coupler_left = GratingCoupler.make_traditional_coupler_at_port(wg1.port, **self.coupler_params)
        coupler_right = GratingCoupler.make_traditional_coupler_at_port(wg2.port, **self.coupler_params)
        cell = Cell(name)
        cell.add_to_layer(1, coupler_left, wg1, wg2, coupler_right)

        return cell

    def amzi(self, difference, name = None):
        if name is None:
            name = 'amzi'
        coupler_left = GratingCoupler.make_traditional_coupler(
            origin=[0, 0],
            **self.coupler_params
        )
        wg1 = Waveguide.make_at_port(coupler_left.port)
        wg1.add_straight_segment(10)
        wg1.add_bend(-pi/2, 20)
        wg1.add_straight_segment(10)

        mmi1 = MMI.make_at_port(wg1.port, 16, 4, 1, 2)
        wg1_1 = Waveguide.make_at_port(mmi1.output_ports[0])
        wg1_1.add_bend(-pi/2, 20)
        wg1_1.add_bend(pi/2, 20)
        wg1_1.add_straight_segment(100)
        wg1_1.add_bend(pi/2, 20)
        wg1_1.add_bend(-pi/2, 20)

        wg1_2 = Waveguide.make_at_port(mmi1.output_ports[1])
        wg1_2.add_bend(pi/2, 20)
        wg1_2.add_straight_segment(difference/2)
        wg1_2.add_bend(-pi/2, 20)
        wg1_2.add_straight_segment(100)
        wg1_2.add_bend(-pi/2, 20)
        wg1_2.add_straight_segment(difference/2)
        wg1_2.add_bend(pi/2, 20)

        mmi2 = MMI.make_at_port(wg1_2.port, 16, 4, 2, 1)

        wg2 = Waveguide.make_at_port(mmi2.output_ports[0])
        wg2.add_straight_segment(10)
        wg2.add_bend(-pi/2, 20)
        wg2.add_straight_segment(10)

        coupler_right = GratingCoupler.make_traditional_coupler_at_port(
            wg2.port,
            **self.coupler_params
        )


        cell = Cell(name)
        cell.add_to_layer(1, coupler_left, wg1, mmi1, wg1_1, wg1_2, mmi2, wg2, coupler_right)

        return cell

    def amzi_converter(self, difference, name = None):
        if name is None:
            name = 'amzi'
        coupler_left = GratingCoupler.make_traditional_coupler(
            origin=[0, 0],
            **self.coupler_params
        )
        wg1 = Waveguide.make_at_port(coupler_left.port)
        wg1.add_straight_segment(10)
        wg1.add_bend(-pi/2, 20)
        wg1.add_straight_segment(10)

        mmi1 = MMI.make_at_port(wg1.port, 16, 4, 1, 2)
        wg1_1 = Waveguide.make_at_port(mmi1.output_ports[0])
        wg1_1.add_bend(-pi/2, 20)
        wg1_1.add_bend(pi/2, 20)
        wg1_1.add_straight_segment(10, 0.5)
        wg1_1_1 = Waveguide.make_at_port(port=Port([wg1_1.port.origin[0]+80, wg1_1.port.origin[1]], 0, 0.5))
        wg1_1_1.add_straight_segment(10, 1.3)
        wg1_1_1.add_bend(pi/2, 20)
        wg1_1_1.add_bend(-pi/2, 20)

        wg1_2 = Waveguide.make_at_port(mmi1.output_ports[1])
        wg1_2.add_bend(pi/2, 20)
        wg1_2.add_straight_segment(difference/2)
        wg1_2.add_bend(-pi/2, 20)
        wg1_2.add_straight_segment(100)
        wg1_2.add_bend(-pi/2, 20)
        wg1_2.add_straight_segment(difference/2)
        wg1_2.add_bend(pi/2, 20)

        mmi2 = MMI.make_at_port(wg1_2.port, 16, 4, 2, 1)

        wg2 = Waveguide.make_at_port(mmi2.output_ports[0])
        wg2.add_straight_segment(10)
        wg2.add_bend(-pi/2, 20)
        wg2.add_straight_segment(10)

        coupler_right = GratingCoupler.make_traditional_coupler_at_port(
            wg2.port,
            **self.coupler_params
        )


        cell = Cell(name)
        cell.add_to_layer(1, coupler_left, wg1, mmi1, wg1_1, wg1_1_1, wg1_2, mmi2, wg2, coupler_right)

        return cell
