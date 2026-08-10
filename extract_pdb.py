#!/usr/bin/env python


from prody import *
import shutil
import os
import glob


# pdb_files = ['1asy', '1ekz', '1di2', '1a9n']
pdb_files = ['1asy', '1a9n', '1b7f', '3wbm', '1av6', '1c9s', '1cvj', '1g2e', '1jbs', '1jid', 
'1k8w', '1knz', '1kq2', '1lng', '1m5o', '1m8v', '1wpu', '1wsu', '1zbh', '2a8v', '2anr', '2asb',
'2b3j', '2bx2', '2db3', '2g4b', '2gic', '2ix1', '2j0s', '2jea', '2jlu', '2py9', '2q66', '2r7r',
'2vnu', '2xgj', '2xnr', '2xs2', '2xzo', '3aev', '3bx2', '3d2s', '3i5x', '3iev', '3k5q', '3mdg',
'3nmr', '3o8c', '3pf4', '3qjj', '3r2c', '3rc8', '3t5n', '4h5p', '4j1g', '4j7m', '4m59', '4mdx',
'4n2q', '5aor', '5det', '5eim', '5elh', '5elk', '5elr', '5els', '5ex7', '5gxh', '5i4a', '5lta',
'1di2', '1hq1', '1msw', '1n35', '1ooa', '1r3e', '1r9f', '1si3', '1wne', '1yvp', '1zbi', '2az0',
'2bgg', '2ez6', '2f8s', '2gjw', '2gxb', '2ozb', '2pjp', '2qux', '2r8s', '2xd0', '2y8w', '2ykg',
'2zi0', '2zko', '3a6p', '3bsn', '3bt7', '3dh3', '3eqt', '3fte', '3iab', '3ks8', '3moj', '3o3i',
'3oij', '3rw6', '3snp', '3zc0', '4ato', '4erd', '4fvu', '4ig8', '4ill', '4l8h', '4zt0', '5aox',
'5ed1', '5f5f', '5f5h', '5id6', '5tf6', '5wtk', '1b23', '1c0a', '1ffy', '1gax', '1h3e', '1h4s',
'1j1u', '1n78', '1qf6', '1qtq', '1ser', '1u0b', '1vfg', '2azx', '2bte', '2csx', '2dlc', '2drb',
'2du3', '2fk6', '2fmt', '2zm5', '2zzm', '3adb', '3amt', '3eph', '3hl2', '3vjr', '4ycp', '4yvj',
'5hr7', '5t8y']
# pdb_files = ['2az0', '1asy']
print("pdb ids: ", len(pdb_files))
# pockets = []
# for i in pdb_files:
# 	p = parsePDB(i)
# 	pocket = p.select('same residue as within 7 of protein and nucleic')
# 	pockets.append(pocket)

# directory_name = "pockets"
# try:
#     os.mkdir(directory_name)
#     print(f"Directory '{directory_name}' created successfully.")
# except FileExistsError:
#     print(f"Directory '{directory_name}' already exists.")
# except PermissionError:
#     print(f"Permission denied: Unable to create '{directory_name}'.")
# except Exception as e:
#     print(f"An error occurred: {e}")

# destination = './pockets'
# files = []
# for f, i in zip(pockets, pdb_files):
# 	file = writePDB(i + "_pocket.pdb", f)
# 	files.append(file)

# for c in files:
# 	shutil.copy(c, destination)

# for filename in glob.glob("*.gz"):
#     os.remove(filename)

# for f in glob.glob("*.pdb"):
# 	os.remove(f)
