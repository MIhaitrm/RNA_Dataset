#!/usr/bin/env python


import numpy as np
from numpy.linalg import norm
import pymesh
from read_msms import read_msms
from sklearn.neighbors import KDTree

vertices, faces, normals, res_id = read_msms('fragment0.xyzr')
mesh = pymesh.form_mesh(vertices, faces)


def fix_mesh(mesh, resolution, detail="normal"):
    bbox_min, bbox_max = mesh.bbox
    diag_len = norm(bbox_max - bbox_min)
    if detail == "normal":
        target_len = diag_len * 5e-3
    elif detail == "high":
        target_len = diag_len * 2.5e-3
    elif detail == "low":
        target_len = diag_len * 1e-2
    
    target_len = resolution
    #print("Target resolution: {} mm".format(target_len));
    # PGC 2017: Remove duplicated vertices first
    mesh, _ = pymesh.remove_duplicated_vertices(mesh, 0.001)


    count = 0;
    print("Removing degenerated triangles")
    mesh, __ = pymesh.remove_degenerated_triangles(mesh, 100);
    mesh, __ = pymesh.split_long_edges(mesh, target_len);
    num_vertices = mesh.num_vertices;
    while True:
        mesh, __ = pymesh.collapse_short_edges(mesh, 1e-6);
        mesh, __ = pymesh.collapse_short_edges(mesh, target_len,
                preserve_feature=True);
        mesh, __ = pymesh.remove_obtuse_triangles(mesh, 150.0, 100);
        if mesh.num_vertices == num_vertices:
            break;

        num_vertices = mesh.num_vertices;
        #print("#v: {}".format(num_vertices));
        count += 1;
        if count > 10: break;

    mesh = pymesh.resolve_self_intersection(mesh);
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    mesh = pymesh.compute_outer_hull(mesh);
    mesh, __ = pymesh.remove_duplicated_faces(mesh);
    mesh, __ = pymesh.remove_obtuse_triangles(mesh, 179.0, 5);
    mesh, __ = pymesh.remove_isolated_vertices(mesh);
    mesh, _ = pymesh.remove_duplicated_vertices(mesh, 0.001)
    
    return mesh

regular_mesh = fix_mesh(mesh, 1.0, 'normal')


# def normalization(data):
#     _range = np.max(data) - np.min(data)
#     return (data - np.min(data)) / _range

# kdt = KDTree(vertices)

# dist, r = kdt.query(regular_mesh.vertices)  
#         # np.save(out_Ply_files + ".npy", dist.T[0])
# dists = normalization(dist).T[0]  


# assert (len(dist) == len(regular_mesh.vertices))
# value_interacte = sum(dist) / len(dist)
#         # value_interacte = float(DiSion_RNA) + 4.0

# iface = np.zeros(len(regular_mesh.vertices))
# iface_v = np.where(dist <= value_interacte)[0]  
# iface[iface_v] = 1.0

# print(iface)