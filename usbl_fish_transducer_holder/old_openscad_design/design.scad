$fa = 1.0;
$fs = 0.5;

ENCLOSURE_DIA = 114.3;
THICKNESS = 6.0;


CABLE_VERT_HOLE_DIA = 25;
CABLE_HORI_HOLE_DIA = 30;
CABLE_HORI_SAFE_HEIGHT = 65;

OUTER_BASE_HEIGHT = 10.0 + CABLE_HORI_SAFE_HEIGHT + 10;
INNER_BASE_HEIGHT = 15.0;
INNER_BASE_DIA = 55.0 + THICKNESS;

CLAMP_HOLE_WIDTH = 15;
CLAMP_HOLE_HEIGHT = 3;
SCREW_DIA = 5;
SCREW_RING_DIA = 35.0;
N_SCREWS = 6;


module outer_base() {
    difference() {
        translate([0, 0, -ENCLOSURE_DIA/2.0])
            cylinder(h=OUTER_BASE_HEIGHT + ENCLOSURE_DIA/2.0, d=    ENCLOSURE_DIA, center=false);
    
        translate([0, 0, -ENCLOSURE_DIA/2.0 - THICKNESS])
            cylinder(h=OUTER_BASE_HEIGHT + ENCLOSURE_DIA/2.0, d=    ENCLOSURE_DIA - THICKNESS * 2, center=false);
    
        translate([0, 0, -ENCLOSURE_DIA/2.0])
            rotate([0, 90, 0])
                cylinder(h=2 * ENCLOSURE_DIA, d=ENCLOSURE_DIA, center=true);
    
        translate([0, 0, -1.25 * ENCLOSURE_DIA/2.0])
            cube(ENCLOSURE_DIA, center=true);
    }
}

module inner_base() {
    
    difference() {
    translate([0, 0, OUTER_BASE_HEIGHT - THICKNESS + 0.001])
        cylinder(h=INNER_BASE_HEIGHT + THICKNESS, d=INNER_BASE_DIA, center=false);        
    }
}

module cable_vert_hole() {
    cylinder(h = OUTER_BASE_HEIGHT * 10, d = CABLE_VERT_HOLE_DIA, center=true);
    
}

module clamp_hole() {
    translate([0, 0, 5.0])
    // rotate([0, 90, 0])
    cube([CLAMP_HOLE_WIDTH, 2 * ENCLOSURE_DIA, CLAMP_HOLE_HEIGHT], center=true);
}

module cable_hori_hole() {
    translate([0, 0, OUTER_BASE_HEIGHT + INNER_BASE_HEIGHT - CABLE_HORI_SAFE_HEIGHT])
    rotate([0, 90, 0])
    cylinder(h = ENCLOSURE_DIA * 2, d = CABLE_HORI_HOLE_DIA, center=true);
}

module screw_hole() {
    cylinder(h=300, d=SCREW_DIA, center=true);
}

module screw_holes() {
    for (i = [1:1:N_SCREWS])
        rotate([0, 0, i * 360.0 / N_SCREWS])
            translate([SCREW_RING_DIA/2.0, 0, 0])
                screw_hole();
}

//color([1.0, 0.0, 0.0, 0.5])
difference () {
    union() {
        outer_base();
        inner_base();
    }

    translate([0, 0, 0])
        cylinder(h=OUTER_BASE_HEIGHT + INNER_BASE_HEIGHT - THICKNESS, d=INNER_BASE_DIA - THICKNESS * 02, center=false);
        
    cable_vert_hole();
    cable_hori_hole();
    clamp_hole();
    screw_holes();
}



