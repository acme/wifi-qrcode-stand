import cadquery as cq

# Nozzle diameter in mm
nozzle_diameter = 0.6

# Layer height in mm
layer_height = 0.2

# Width/height of the QR code in mm
size = 50


# Calculate the extrusion width that PrusaSlicer defaults use
def calculate_extrusion_width(nozzle_diameter):
    if nozzle_diameter == 0.4:
        return nozzle_diameter * 1.125
    elif nozzle_diameter == 0.6:
        return nozzle_diameter
    else:
        print("Not sure what the extrusion width should be, using nozzle diameter")
        return nozzle_diameter


# Calculate the thickness of the shell in mm
# This is the recommend object thin wall thickness the layer height
# with 4 lines
# https://manual.slic3r.org/advanced/flow-math
def calculate_shell_thickness(layer_height, extrusion_width):
    return (extrusion_width - layer_height * (1 - (3.141 / 4))) * 3 + extrusion_width


# The extrusion width in mm
extrusion_width = calculate_extrusion_width(nozzle_diameter)

# The thickness of the shell in mm
thickness = calculate_shell_thickness(layer_height, extrusion_width)

print("Thickness: ", thickness)

points = [
    (-size, size / 4),
    (0, 0),
    (0, size / 4),
]

stand = (
    cq.Workplane()
    .polyline(points)
    .close()
    .offset2D(thickness)
    .extrude(size)
    .faces("+Z or -Z")
    .shell(thickness)
)

show_object(stand, options={"alpha": 0.0, "color": (255, 108, 47)})

# Export the object
cq.exporters.export(stand, f"stand-{nozzle_diameter}mm-{layer_height}mm.3mf")
cq.exporters.export(stand, f"stand-{nozzle_diameter}mm-{layer_height}mm.step")
cq.exporters.export(stand, f"stand-{nozzle_diameter}mm-{layer_height}mm.stl")
