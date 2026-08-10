#!/usr/bin/env python

import numpy as np
import pymesh
# from save_ply import vertices, faces
import networkx as nx
import os
import glob
import csv
import shutil

path = "ply_files"
files = glob.glob(os.path.join(path, "*.ply"))

meshes = []
for f in files:
	mesh = pymesh.load_mesh(f)
	meshes.append(mesh)

def get_edges(mesh):
	G = nx.Graph()
	n = len(mesh.vertices)
	G.add_nodes_from(np.arange(n))
	f = np.array(mesh.faces, dtype=int)
	rowi = np.concatenate([f[:,0], f[:,0], f[:,1], f[:,1], f[:,2], f[:,2]], axis=0)
	rowj = np.concatenate([f[:,1], f[:,2], f[:,0], f[:,2], f[:,0], f[:,1]], axis=0)
	edges = np.stack([rowi, rowj]).T
	return edges

# edges = get_edges(mesh)
# print(edges)

edges = []
for m in meshes:
	edge = get_edges(m)
	edges.append(edge)

for idx, e in enumerate(edges):
	with open(f"edge_file{idx}.tsv", 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		writer.writerows(e)


directory_name = "edge_dir"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

destination = './edge_dir'

for c in glob.glob("*.tsv"):
    shutil.copy(c, destination)

for name in glob.glob("*.tsv"):
    os.remove(name)

# vertices = mesh.vertices

# with open('vert.tsv', 'w') as v:
# 	writer = csv.writer(v, delimiter='\t')
# 	writer.writerows(vertices)