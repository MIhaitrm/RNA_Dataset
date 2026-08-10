#!/usr/bin/env python

"""
read_ply.py: Save a ply file to disk using pymesh and load the attributes used by MaSIF. 
Pablo Gainza - LPDI STI EPFL 2019
Released under an Apache License 2.0
"""

import pymesh
import numpy
from read_msms import read_msms
from compute_theta import compute_theta
import glob
import os
from computeMSMS import computeMSMS
import shutil
import re

path = "fragments"
ids = glob.glob(os.path.join(path, "*.xyzr"))

v = []
f = []
n = []
nm = []
vt = []

for i in ids:
    vertices, faces, normals, names = read_msms(i)
    vertex_theta = compute_theta(vertices, normals)
    v.append(vertices)
    f.append(faces)
    n.append(normals)
    nm.append(names)
    vt.append(vertex_theta)

def save_ply(
    filename,
    vertices,
    faces=[],
    normals=None,
    vertex_theta=None,
):
    """ Save vertices, mesh in ply format.
        vertices: coordinates of vertices
        faces: mesh
    """
    mesh = pymesh.form_mesh(vertices, faces)
    if normals is not None:
        n1 = normals[:, 0]
        n2 = normals[:, 1]
        n3 = normals[:, 2]
        mesh.add_attribute("vertex_nx")
        mesh.set_attribute("vertex_nx", n1)
        mesh.add_attribute("vertex_ny")
        mesh.set_attribute("vertex_ny", n2)
        mesh.add_attribute("vertex_nz")
        mesh.set_attribute("vertex_nz", n3)
    if vertex_theta is not None:
        mesh.add_attribute("vertex_theta")
        mesh.set_attribute("vertex_theta", vertex_theta)

    pymesh.save_mesh(
        filename, mesh, *mesh.get_attribute_names(), use_float=True, ascii=True
    )


for x, vert, face, norm, theta in zip(ids, v, f, n, vt):
    save_ply(x + ".ply", vert, face, norm)

p = "fragments"
destination = "./ply_files"
for y in glob.glob(os.path.join(p, "*.ply")):
    shutil.move(y, destination)

new_names = []
for name in glob.glob(os.path.join("ply_files", "*.ply")):
    new_name = re.sub(r".xyzr", "", name)
    new_names.append(new_name)

# print(new_names)

destination = glob.glob(os.path.join("ply_files", "*.ply"))


for b, c in zip(new_names, destination):
    os.rename(c, b)


# directory_name = "ply_files"
# try:
#     os.mkdir(directory_name)
#     print(f"Directory '{directory_name}' created successfully.")
# except FileExistsError:
#     print(f"Directory '{directory_name}' already exists.")
# except PermissionError:
#     print(f"Permission denied: Unable to create '{directory_name}'.")
# except Exception as e:
#     print(f"An error occurred: {e}")

# destination = "ply_files"

# for f in glob.glob("*.ply"):
#     shutil.copy(f, destination)

# for fi in glob.glob("*.ply"):
#     os.remove(fi)