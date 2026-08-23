// PRAYCG ALS-PT19 40x40mm Flanged Shroud (Upper-Left Inset)
// All units in mm

// --- PARAMETERS ---
flange_size = 40.0;     // 40mm x 40mm outer light-blocking base
flange_thickness = 1.0; // Thickness of the tape flange
edge_inset = 3.0;       // Inset distance from top and left flange edges

sensor_width = 10.5;    // 10.1mm + 0.4mm printer shrinkage tolerance
sensor_height = 7.9;    // 7.5mm + 0.4mm printer shrinkage tolerance
cavity_depth = 6.0;     // Depth to swallow the sensor body
wall_thickness = 1.5;   // Solid walls to prevent light leakage
wire_hole_dia = 4.0;    // Wire passthrough hole

$fn = 64; // High resolution for smooth curves

// Derived outer housing dimensions
housing_w = sensor_width + 2 * wall_thickness;
housing_h = sensor_height + 2 * wall_thickness;

// Position housing in the upper-left quadrant
pos_x = -flange_size/2 + edge_inset;
pos_y =  flange_size/2 - edge_inset - housing_h;

// --- GEOMETRY ---
union() {
    difference() {
        // 1. Outer Geometry (Flange Base + Housing Block)
        union() {
            // Flat 40x40mm screen contact flange
            translate([-flange_size/2, -flange_size/2, 0])
                cube([flange_size, flange_size, flange_thickness]);
            
            // Inset sensor housing block
            translate([pos_x, pos_y, 0])
                cube([housing_w, housing_h, cavity_depth + wall_thickness]);
        }
        
        // 2. Sensor Cavity Cutout (Front opening)
        translate([pos_x + wall_thickness, pos_y + wall_thickness, -0.1])
            cube([sensor_width, sensor_height, cavity_depth + 0.1]);
            
        // 3. Centered Wire Exit Hole (Through back wall)
        translate([pos_x + housing_w/2, pos_y + housing_h/2, cavity_depth - 0.1])
            cylinder(h = wall_thickness + 0.5, d = wire_hole_dia);
    }
    
    // 4. Strain Relief Zip-Tie Anchor (Facing inward toward the flange body)
    translate([pos_x + housing_w - 4, pos_y - 4, cavity_depth]) {
        difference() {
            // Anchor block
            cube([4, 5, 5]); 
            // Zip-tie channel
            translate([-1, 2.5, 2.5])
                rotate([0, 90, 0])
                cylinder(h = 6, d = 2.5);
        }
    }
}