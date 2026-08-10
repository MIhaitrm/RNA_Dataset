#!/usr/bin/env python

import csv
import os
import glob

files = glob.glob("*.pt")
print(files)


# for f in files:
# with open("annotation_file.csv", "w") as file:
# 	writer = csv.writer(file)
# 	writer.writerow(files)


with open('annotation_file.csv', 'w') as f:
    for line in files:
        f.write(f"{line}\n")