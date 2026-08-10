#!/usr/bin/env python

import numpy as np
from read_msms import read_msms
from compute_normal import compute_normal, crossp
import math

# vertices, faces, normalv, res_id = read_msms('fragments/fragment0.xyzr')
# normals = compute_normal(vertices, faces)

# print(vertices.shape)

# theta = []
# for i,j in zip(vertices, normals):
# 	dot_product = np.dot(i, j)
# 	magnitude_A = np.linalg.norm(i)
# 	magnitude_B = np.linalg.norm(j)
# 	angle_radians = np.arccos(dot_product / (magnitude_A * magnitude_B))
# 	angle_degrees = np.degrees(angle_radians)
# 	theta.append(angle_degrees)

# #print(theta)
# print(isinstance(theta, list))
# theta = np.array(theta)
# print(theta)


## https://stackoverflow.com/questions/50772176/calculate-the-angle-between-the-rows-of-two-matrices-in-numpy
def compute_theta(vertices, normals):
    p1 = np.einsum('ij,ij->i',vertices,normals)
    p2 = np.linalg.norm(vertices,axis=1)
    p3 = np.linalg.norm(normals,axis=1)
    p4 = p1 / (p2*p3)
    rad = np.arccos(np.clip(p4,-1.0,1.0))
    deg = np.degrees(rad)
    return deg
# 
# compute_theta(vertices, normals)

# def compute_theta(vertices, normals):
# 	dot_product = crossp(vertices, normals)
# 	print(dot_product)
# 	p2 = np.linalg.norm(vertices,axis=1)
# 	print(p2)
# 	p3 = np.linalg.norm(normals,axis=1)
# 	print(p3)
# 	p4 = dot_product / (p2*p3)
# 	rad = np.arccos(np.clip(p4,-1.0,1.0))
# 	deg = np.degrees(rad)
# 	return deg

# theta = compute_theta(vertices, normals)
# print(theta)