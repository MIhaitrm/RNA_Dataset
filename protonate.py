#!/usr/bin/env python

# import enzy_htp.structure as struct
# import os
# from enzy_htp.preparation import protonate_stru

# # path = "data"
# # dir_list = os.listdir(path)
# # print(dir_list)

# # for x in dir_list:
# # 	print(x)
# # 	sp = struct.PDBParser()
# # 	stru = sp.get_structure(x)
# # 	print(stru.num_atoms)
# # 	protonate_stru(stru=stru)
# # 	print(stru.num_atoms)


# sp = struct.PDBParser()
# filepath = '3wbm.pdb'
# stru = sp.get_structure(filepath)
# protonate_stru(stru=stru)

from subprocess import Popen, PIPE
from IPython.core.debugger import set_trace
import os
from extract_pdb import pdb_files
import glob
import shutil


def protonate(in_pdb_file, out_pdb_file):
    # protonate (i.e., add hydrogens) a pdb using reduce and save to an output file.
    # in_pdb_file: file to protonate.
    # out_pdb_file: output file where to save the protonated pdb file. 
    
    # Remove protons first, in case the structure is already protonated
    args = ["reduce", "-Trim", in_pdb_file]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    outfile = open(out_pdb_file, "w")
    outfile.write(stdout.decode('utf-8').rstrip())
    outfile.close()
    # Now add them again.
    args = ["reduce", "-HIS", out_pdb_file]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    outfile = open(out_pdb_file, "w")
    outfile.write(stdout.decode('utf-8'))
    outfile.close()


path = "pockets"
filename = "*.pdb"
pdbs = glob.glob(os.path.join(path, "*.pdb"))
print(isinstance(pdbs, list))
print(pdbs)

h = "H.pdb"
prot_data = []
for i in pdbs:
    file = i.removesuffix("_pocket.pdb")
    prot_data.append(file)


ids = []
for m in prot_data:
    fi = m.removeprefix("pockets/")
    ids.append(fi)
print(ids)

prot_data = [f + h for f in ids]
print(prot_data)


for input_file, output_file in zip(pdbs, prot_data):
    protonate(input_file, output_file)


directory_name = "protonated"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

destination = './protonated'

for c in glob.glob("*H.pdb"):
    shutil.copy(c, destination)

for name in glob.glob("*H.pdb"):
    os.remove(name)

