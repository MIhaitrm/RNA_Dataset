#!/usr/bin/env python

import numpy as np
import pymesh
from save_ply import vertices, faces
import networkx as nx
import os
import glob
import csv
import shutil

# path = "ply_files"
# files = glob.glob(os.path.join(path, "*.ply"))

# meshes = []
# for f in files:
# 	mesh = pymesh.load_mesh(f)
# 	meshes.append(mesh)

# def get_vertices(mesh):
# 	G = nx.Graph()
# 	vertices = mesh.vertices
# 	return vertices

# verts = []
# for m in meshes:
# 	v = get_vertices(m)
# 	verts.append(v)

# for idx, e in enumerate(verts):
# 	with open(f"vert_file{idx}.tsv", 'w') as f:
# 		writer = csv.writer(f, delimiter='\t')
# 		writer.writerows(e)

# directory_name = "verts_dir"
# try:
#     os.mkdir(directory_name)
#     print(f"Directory '{directory_name}' created successfully.")
# except FileExistsError:
#     print(f"Directory '{directory_name}' already exists.")
# except PermissionError:
#     print(f"Permission denied: Unable to create '{directory_name}'.")
# except Exception as e:
#     print(f"An error occurred: {e}")

# destination = './verts_dir'

# for c in glob.glob("*.tsv"):
#     shutil.copy(c, destination)

# for name in glob.glob("*.tsv"):
#     os.remove(name)

path = "feature_files"
files = glob.glob(os.path.join(path, "*.npy"))