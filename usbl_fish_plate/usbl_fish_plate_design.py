"""
This module contains a design for an electronics housing inside a
sealed container, used in under-water comm. research using USBL.
The device is aptly named 'fish'. This work was produced for
'Autonomous Field Robotics Lab' in University of South Carolina.

Author: Titon Barua <baruat@email.sc.edu>
"""

import sys
from build123d import *
from ocp_vscode import *

inch = 25.4 # inch -> mm

plate_length = 290.0
plate_width = 100.0
plate_thickness = 5.3

front_cut_width = 38
back_cut_width = 14
cut_y_locs = (
    (plate_width/2 - 10, plate_width/2),
    (-17.5, 17.5),
    (-plate_width/2, -plate_width/2 + 10))

rpi4_x = -plate_length/2 + 130
rpi4_screw_hole_props = {
    "dia": 2.9, #M2.5, normal fit
    "dist_l": 58,
    "dist_w": 49,
}

adafruit_icm20948_x = plate_length/2 - 50
adafruit_icm20948_screw_hole_props = {
    "dia": 2.9, # M2.5, normal fit
    "dist_l": 0.8 * inch,
    "dist_w": 0.5 * inch,
}

clenna_dc_dc_converter_x = -plate_length/2 + 55
clenna_dc_dc_converter_screw_hole_props = {
    "dia": 5.3,
    "dist": 65,
}


def create_quad_screw_holes(props):
    h = plate_thickness * 2
    p = props
    d, l, w = p["dia"], p["dist_l"], p["dist_w"]
    l2 = l/2
    w2 = w/2
    locs = Locations((-l2, -w2), (l2, -w2), (-l2, w2), (l2, w2))
    return Part() + locs * Cylinder(d/2, h)


def create_dual_screw_holes(props):
    h = plate_thickness * 2
    p = props
    d, w = p["dia"], p["dist"]
    locs = Locations((0, w/2), (0, -w/2))
    return Part() + locs * Cylinder(d/2, h)


def create_front_back_cuts(front):
    cut_boxes = []
    w = front_cut_width if front else back_cut_width
    w_offset = -w/2 if front else w/2
    for y1, y2 in cut_y_locs:
        cut_boxes.append(
            Pos(w_offset, (y1 + y2)/2.0)
            * Box(w, y2 - y1, plate_thickness))
    return Part() + cut_boxes


def create_slot(length, dia):
    return extrude(
        SlotCenterToCenter(length, dia),
        both=True,
        amount=plate_thickness)


def create_design():
    plate = Box(plate_length, plate_width, plate_thickness)

    # Create rectangular cuts in front and back.
    plate -= Pos(plate_length/2, 0) * create_front_back_cuts(True)
    plate -= Pos(-plate_length/2, 0) * create_front_back_cuts(False)

    # Create screw holes for IMU.
    plate -= (
        Pos(adafruit_icm20948_x, 0)
        * Rot(Z=90)
        * create_quad_screw_holes(
            adafruit_icm20948_screw_hole_props))

    # Create power converter screw holes.
    plate -= (
        Pos(clenna_dc_dc_converter_x, 0)
        * Rot(Z=90)
        * create_dual_screw_holes(
            clenna_dc_dc_converter_screw_hole_props))

    # Create RPI4 screw holes.
    plate -= (
        Pos(rpi4_x, 0)
        * create_quad_screw_holes(
            rpi4_screw_hole_props))

    # Add some slots for weight reduction and shock absorbtion.
    plate -= Pos(rpi4_x) * Rot(Z=45) * create_slot(30, 5)
    plate -= Pos(rpi4_x) * Rot(Z=-45) * create_slot(30, 5)
    plate -= Pos(clenna_dc_dc_converter_x) * Rot(Z=0) * create_slot(30, 5)
    plate -= Pos(clenna_dc_dc_converter_x) * Rot(Z=90) * create_slot(30, 5)

    # Cut some cable routing holes.
    plate -= Pos(rpi4_x, plate_width/2) * create_slot(40, 25)
    plate -= Pos(rpi4_x, -plate_width/2) * create_slot(40, 25)
    plate -= Pos(plate_length/4, plate_width/5) * Rot(Z=60) * create_slot(15, 15)
    plate -= Pos(plate_length/4, -plate_width/5) * Rot(Z=-60) * create_slot(15, 15)
    plate -= Pos(plate_length/4 - 40, 0) * Rot(Z=0) * create_slot(15, 15)

    # Do some rounding of the edges.
    plate = fillet(
        plate.edges().filter_by(Axis.Z),
        radius=2.5)
    plate = chamfer(
        plate.edges()
            .filter_by(Plane.XY)
            .group_by(Axis.Z)[-1],
        length=0.5)

    # "... cause it feels so empty without me ..." - eminem
    text = Text(
        "Designed in UofSC",
        font_size=6)
    plate -= Pos(
        plate_length/2.0 - 30,
        3*plate_width/8 - 9,
        plate_thickness/2) * extrude(text, amount=-1.0)

    return plate


if __name__ == "__main__":
    design = create_design() 
    if len(sys.argv) < 2:
        show(design)
        
    elif sys.argv[1] == "export_stl":
        export_path = sys.argv[2]
        export_stl(design, export_path)