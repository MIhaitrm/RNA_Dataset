#!/usr/bin/env python


import pymesh
import time
import numpy as np
import glob
import os
import shutil
from compute_polar_coordinates import compute_polar_coordinates
from save_ply import save_ply

from sklearn import metrics
import pymesh

# mesh = pymesh.load_mesh('1b7f.ply')
# mesh.add_attribute('vertex_normal')
# normals = mesh.get_attribute('vertex_normal')
# print(normals)

# print(mesh.vertices)

def read_data_from_surface(ply_fn):
	mesh = pymesh.load_mesh(ply_fn)

	mesh.add_attribute('vertex_normal')
	normals = mesh.get_attribute('vertex_normal')

	rho, theta, neigh_indices, mask = compute_polar_coordinates(mesh, radius=9, max_vertices=100)
	# print("Rho: ", rho)
	# print("Mask: ", mask)

	mesh.add_attribute('vertex_mean_curvature')
	H = mesh.get_attribute('vertex_mean_curvature')
	mesh.add_attribute('vertex_gaussian_curvature')
	K = mesh.get_attribute('vertex_gaussian_curvature')

	elem = np.square(H) - K

	elem[elem<0] = 1e-8

	k1 = H + np.sqrt(elem)

	k2 = H - np.sqrt(elem)

	si = (k1+k2)/(k2-k1)
	si = np.arctan(si)*(2/np.pi)

	n = len(mesh.vertices)

	input_feat = np.zeros((n, 100, 2))

	for vix in range(n):
		neigh_vix = np.array(neigh_indices[vix])
		patch_v = mesh.vertices[neigh_vix]
		# print(patch_v.shape)
		patch_n = normals[neigh_vix]
		patch_cp = np.where(neigh_vix == vix)[0][0] # central point
		mask_pos = np.where(mask[vix] == 1.0)[0] # nonzero elements
		patch_rho = rho[vix][mask_pos] # nonzero elements of rho
		ddc = compute_ddc(patch_v, patch_n, patch_cp, patch_rho)  
		# print("DDC Shape:", ddc.shape)      
		input_feat[vix, :len(neigh_vix), 0] = si[neigh_vix]
		# print("SI shape:", si[neigh_vix].shape)
		# print("input_feat shape:", input_feat.shape)
		input_feat[vix, :len(neigh_vix), 1] = ddc
		# print("Input feat:", input_feat)

	return input_feat, rho, theta, mask, neigh_indices, np.copy(mesh.vertices)

def extract_patch_and_coord(
    vix, shape, coord, max_distance, max_vertices, patch_indices=False
):
    # Member vertices are nonzero elements
    i, j = coord[np.int(vix), : coord.shape[1] // 2].nonzero()


    # D = np.squeeze(np.asarray(coord[np.int(vix),j].todense()))
    D = np.squeeze(np.asarray(coord[np.int(vix), : coord.shape[1] // 2].todense()))
    j = np.where((D < max_distance) & (D > 0))[0]
    max_dist_tmp = max_distance
    old_j = len(j)
    while len(j) > max_vertices:
        max_dist_tmp = max_dist_tmp * 0.95
        j = np.where((D < max_dist_tmp) & (D > 0))[0]
    #    print('j = {} {}'.format(len(j), old_j))
    D = D[j]
    patch = {}
    patch["X"] = shape["X"][0][j]
    patch["Y"] = shape["Y"][0][j]
    patch["Z"] = shape["Z"][0][j]
    patch["normal"] = shape["normal"][:, j]
    patch["shape_index"] = shape["shape_index"][0][j]

    patch["center"] = np.argmin(D)

    j_theta = j + coord.shape[1] // 2
    theta = np.squeeze(np.asarray(coord[np.int(vix), j_theta].todense()))
    coord = np.concatenate([D, theta], axis=0)

    if patch_indices:
        return patch, coord, j
    else:
        return patch, coord

def mean_normal_center_patch(D, n, r):
	c_normal = [n[i] for i in range(len(D)) if D[i] <= r]
	mean_normal = np.mean(c_normal, axis=0, keepdims=True).T
	mean_normal = mean_normal / np.linalg.norm(mean_normal)
	return np.squeeze(mean_normal)

def compute_ddc(patch_v, patch_n, patch_cp, patch_rho):
	n = patch_n
	n = np.expand_dims(n, axis = 1)
	r = patch_v
	i = patch_cp
	ni = mean_normal_center_patch(patch_rho, n, 2.5)
	dij = np.linalg.norm(r - r[i], axis=1)
	sf = r + n
	sf = sf - (ni + r[i])
	sf = np.linalg.norm(sf, axis=1)
	sf = sf - dij
	sf[sf > 0] = 1
	sf[sf < 0] = -1
	sf[sf == 0] = 0
	dij[dij == 0] = 1e-8
	kij = np.divide(np.linalg.norm(n - ni, axis=1), dij)
	kij = np.multiply(sf, kij)
	kij[kij > 0.7] = 0
	kij[kij < -0.7] = 0

	return kij


# read_data_from_surface('1asy.ply')
path = "ply_files"

files = glob.glob(os.path.join(path, "*.ply"))
for i in files:
	print("Ply files:", i)


features = []
for f in files:
	input_feat, rho, theta, mask, neigh_indices, copy = read_data_from_surface(f)
	si = input_feat[:,:,0]
	ddc = input_feat[:,:,1]
	# new_axis = (-1)
	# rho = np.expand_dims(rho, axis=new_axis)
	# theta = np.expand_dims(theta, axis=new_axis)
	feature = np.concatenate([si, ddc, rho, theta], axis=1)
	features.append(feature)
# 	print("SI shape: ",si.shape)
# 	print("DDC shape: ", ddc.shape)
# 	print("Rho shape: ", rho.shape)
# 	print("Theta shape: ", theta.shape)

for idx, feat in enumerate(features):
	with open(f"feature{idx}.npy", "wb") as ft:
		np.save(ft, feat)

directory_name = "feature_files"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

destination = "feature_files"

for f in glob.glob("*.npy"):
    shutil.copy(f, destination)

for fi in glob.glob("*.npy"):
    os.remove(fi)

# print("Input_feat:", input_feat)

# with open('1b7f.npy', 'wb') as f:
# 	np.save(f, input_feat)