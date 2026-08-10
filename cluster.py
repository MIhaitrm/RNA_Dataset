#!/usr/bin/env python


from sklearn.metrics import pairwise_distances
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
from sklearn.cluster import DBSCAN
import hdbscan
import matplotlib.pyplot as plt
from read_xyzr import xyz_files
import time
import glob
import os
from sklearn.cluster import AgglomerativeClustering
import IPython
import sys
import csv
import shutil

print(xyz_files)
dist_matrices = []

for f in xyz_files:
	dist_matrix = pairwise_distances(f)
	dist_matrices.append(dist_matrix)

start = time.time()

hlabs = []
for i in dist_matrices:
	clustering = AgglomerativeClustering(distance_threshold=4, n_clusters=None, metric='precomputed', linkage='single').fit(i)
	hlab = clustering.labels_
	hlabs.append(hlab)

# print("Hlabs:", hlabs)
for i in hlabs:
	print(i)
end = time.time()

print(f"AgglomerativeClustering ran for {end-start} seconds")

# directory_name = "labels"
# try:
#     os.mkdir(directory_name)
#     print(f"Directory '{directory_name}' created successfully.")
# except FileExistsError:
#     print(f"Directory '{directory_name}' already exists.")
# except PermissionError:
#     print(f"Permission denied: Unable to create '{directory_name}'.")
# except Exception as e:
#     print(f"An error occurred: {e}")

# destination = './labels'
# files = []
# for idx, i in enumerate(hlabs):
# 	with open(f'file{idx}.csv', 'w') as csvfile:
# 		writer = csv.writer(csvfile)
# 		writer.writerows(i)

# for c in files:
# 	shutil.copy(c, destination)

# for filename in glob.glob("*.csv"):
#     os.remove(filename)

# for f in glob.glob("*.pdb"):
	# os.remove(f)

# for h in hlabs:
# 	with np.printoptions(threshold=sys.maxsize):
# 		print(np.array(h))


# start = time.time()

# hscan = list(hdbscan.HDBSCAN(min_cluster_size=10, cluster_selection_epsilon=2).fit(d for d in dist_matrices))
# hlab = hscan.labels_
# hlabs = []
# for d in hlab:
	# hlabs.append(d)

# end = time.time()

# hscans = []
# for i in dist_matrices:
# 	hscan = hdbscan.HDBSCAN(min_cluster_size=10, cluster_selection_epsilon=2).fit(i)
# 	hscans.append(hscan)

# hlabels = []
# for h in hscans:
# 	hlab = h.labels_
# 	hlabels.append(hlab)

# hlabs = []
# for d in hlabels:
# 	hlabs.append(d)


# print(f"HDBSCAN ran for {end-start} seconds")

