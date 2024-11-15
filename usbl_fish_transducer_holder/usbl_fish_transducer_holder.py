"""
This module contains a mount bracket to attach an EvoLogics S2CR 18/34 USBL
transducer around a "BlueRobotics 4inch Water-tight enclosure". The bracket is
shaped to wrap around the cylinder and is held in place using two worm-gear
clamps. This holder was part of the in-house `fish` system, built for underwater
communication research.

The original openscad design was produced for 'Autonomous Field Robotics Lab'
in University of South Carolina. It's available in `old_openscad_design` folder.
This is a re-implmentation with excess bulk removed and improved claming points.

Author: Titon Barua <baruat@email.sc.edu>
"""

import sys
from build123d import *
from ocp_vscode import *

# Design parameters.
# ------------------------------------------,
# Information from https://bluerobotics.com/store/watertight-enclosures/locking-series/wte-locking-tube-r1-vp/
enclosure_props = {
    "outer_dia": 114.3,
    "inner_dia": 101.6,
    "length": 300,
}

shell_thickness = 6
anchor_to_seat_dist = 30
cable_routing_hole_dia = 15 

anchor_props = {
    "dia": 3/4 * enclosure_props["outer_dia"],
    "thinnest_h": 10,
}

transducer_seat_props = {
    "dia": 55 + shell_thickness,
    "cable_hole_dia": 25,
    "n_screws": 6,
    "screw_dia": 5,
    "screw_placement_ring_dia": 35,
    "z_offset": (
        anchor_props["thinnest_h"]
        + anchor_to_seat_dist
        + shell_thickness/2)
}
# ------------------------------------------'


def create_mock_enclosure():
    do = enclosure_props["outer_dia"]
    di = enclosure_props["inner_dia"]
    l = enclosure_props["length"]

    enc = Cylinder(radius=do/2, height=l)
    enc -= Cylinder(radius=di/2, height=l)
    return enc


def create_anchor():
    d = anchor_props["dia"]
    th = anchor_props["thinnest_h"]
    edo = enclosure_props["outer_dia"]
    trans_zoffset = transducer_seat_props["z_offset"]

    # Create handles.
    handles = Box(length=d * 1.75, width=d/3, height=th * 2)
    # Subtract handle grip.
    handle_grip = (
        Pos(Z=-edo/2)
        * Rot(Y=90)
        * Torus(major_radius=edo/2 + 20, minor_radius=15))
    handles -= Pos(X=2/3 * d) * handle_grip
    handles -= Pos(X=-2/3 * d) * handle_grip

    # Anchor base.
    anc = Pos(Z=th - edo/4) * Cylinder(radius=d/2, height=edo/2)
    anc += Rot(Z=90) * handles
    anc -= (
        Pos(Z=th - edo/4)
        * Cylinder(radius=d/2 - shell_thickness, height=edo/2))

    # Subtract enclosure shape.
    anc -= (
        Pos(Z=-edo/2)
        * Rot(X=90)
        * Cylinder(radius=edo/2, height=d * 4))

    anc = fillet(anc.edges().filter_by(Axis.Z), radius=4)

    return anc


def create_transducer_seat():
    d = transducer_seat_props["dia"]
    sn = transducer_seat_props["n_screws"]
    sd = transducer_seat_props["screw_dia"]
    srd = transducer_seat_props["screw_placement_ring_dia"]
    zoffset = transducer_seat_props["z_offset"]
    chd = transducer_seat_props["cable_hole_dia"]

    seat = Cylinder(radius=d/2, height=shell_thickness)
    seat -= Cylinder(radius=chd/2, height=shell_thickness * 2)
    screw_locs = PolarLocations(radius=srd/2, count=sn)
    screw_holes = screw_locs * Cylinder(radius=sd/2, height=shell_thickness * 2)
    seat -= screw_holes
    seat = Pos(Z=zoffset) * seat

    return seat


def create_connecting_struts():
    ad = anchor_props["dia"]
    ath = anchor_props["thinnest_h"]
    sd = transducer_seat_props["dia"]
    h = anchor_to_seat_dist + shell_thickness

    anchor_shape_o = Circle(radius=ad/2)
    anchor_shape_i = Circle(radius=ad/2 - shell_thickness)
    seat_shape_o = Pos(Z=h) * Circle(radius=sd/2)
    seat_shape_i = Pos(Z=h) * Circle(radius=sd/2 - shell_thickness)

    struts = loft([anchor_shape_o, seat_shape_o])
    struts -= loft([anchor_shape_i, seat_shape_i])

    rw = ad/5 # strut width.
    struts = split(struts, Plane.XZ.offset(rw/2), Keep.BOTTOM)
    struts = split(struts, Plane.XZ.offset(-rw/2), Keep.TOP)

    struts1 = Rot(Z=45) * struts
    struts2 = Rot(Z=-45) * struts
    
    return Pos(Z=ath) * (struts1 + struts2)


def create_cable_routing_holes():
    edo = enclosure_props["outer_dia"]
    ath = anchor_props["thinnest_h"]
    d = cable_routing_hole_dia
    holes = (
        Pos(Z=-edo/2)
        * Rot(Z=90)
        * Rot(Y=90)
        * Torus(major_radius=edo/2 + ath*2, minor_radius=d/2))

    return holes


def create_design():
    design = Part()
    design += create_transducer_seat()
    design += create_anchor()
    design += create_connecting_struts()
    design -= create_cable_routing_holes()

    # Cut the weak curve from underneath for ease of 3D printing.
    ath = anchor_props["thinnest_h"]
    design = split(design, Plane.XY.offset(-ath), Keep.TOP)


    return design


if __name__ == "__main__":
    design = create_design() 
    mock_enclosure = (
        Pos(Z=-enclosure_props["outer_dia"]/2)
        * Rot(X=90)
        * create_mock_enclosure())
    
    if len(sys.argv) < 2:
        show_all()
        
    elif sys.argv[1] == "export_stl":
        export_path = sys.argv[2]
        export_stl(design, export_path)