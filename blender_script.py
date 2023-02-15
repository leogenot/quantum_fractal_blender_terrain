import sys
import os

path_to_pillow = '/opt/homebrew/lib/python3.10/site-packages'
sys.path.append(path_to_pillow)

import PIL
from PIL import Image

print(PIL.__file__)

import bpy
import numpy as np

# Load the height map image
img = Image.open('/Users/leogenot/Downloads/Visualizing-Quantum-Computing-using-fractals-main/quantum-fractals-one-complex-number/heightmap.png')
height_map = np.array(img)[:,:,0]

# Check if terrain object exists in scene
if bpy.data.objects.get("Terrain"):
    # Remove terrain object from scene
    bpy.data.objects.remove(bpy.data.objects["Terrain"], do_unlink=True)


# Create a new mesh object
mesh = bpy.data.meshes.new('Terrain')

# Generate vertices and faces
verts = []
faces = []

for x in range(height_map.shape[0]):
    for y in range(height_map.shape[1]):
        z = height_map[x][y] / 15  # Scale the height by a factor of 10
        verts.append((x, y, -z))

        if x < height_map.shape[0] - 1 and y < height_map.shape[1] - 1:
            a = x * height_map.shape[1] + y
            b = a + height_map.shape[1]
            c = b + 1
            d = a + 1
            faces.append((a, b, c, d))

# Create the mesh
mesh.from_pydata(verts, [], faces)
mesh.update()

# Create a new object and link it to the scene
obj = bpy.data.objects.new('Terrain', mesh)
bpy.context.scene.collection.objects.link(obj)

mesh = obj.data
for f in mesh.polygons:
    f.use_smooth = True

# Center the object at the origin
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
obj.location = (-(height_map.shape[0]-1)/2, -(height_map.shape[1]-1)/2, 0)


def set_location(name, xyz):
     bpy.data.objects[name].location = xyz

def set_euler_rotation(name, xyz):
    bpy.data.objects[name].rotation_euler = xyz

def set_scale(name, xyz):
    bpy.data.objects[name].scale = xyz

set_location("Terrain", (0, 0, 0))
#set_euler_rotation("Terrain", (3.1415 * 0.5, 3.1415 * 0.5 * 3, 3.1415 * 0.5 * 0.5))
set_scale("Terrain", (0.05,0.05,0.31))



# Add material
auto_mat = bpy.data.materials["AutoMaterial"]
terrain = bpy.data.objects['Terrain']
terrain.active_material = auto_mat

from os import path

# Set the output image path and file format
""" output_path = "/Users/leogenot/Downloads/Visualizing-Quantum-Computing-using-fractals-main/quantum-fractals-one-complex-number/renders/output_image.png"
i = 0
while path.exists(output_path):
    output_path = "/Users/leogenot/Downloads/Visualizing-Quantum-Computing-using-fractals-main/quantum-fractals-one-complex-number/renders/output_image_{i + 1}.png"
 """

counter = 0
output_path = "/Users/leogenot/Downloads/Visualizing-Quantum-Computing-using-fractals-main/quantum-fractals-one-complex-number/renders/output{}.png"
while os.path.isfile(output_path.format(counter)):
    counter += 1
output_path = output_path.format(counter)
# Adjust the file system permissions to allow writing to the output directory
os.chmod(os.path.dirname(output_path), 0o777)

# Set the output path and file format in the Blender scene
bpy.context.scene.render.filepath = output_path
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Render the scene
bpy.ops.render.render(write_still=True)