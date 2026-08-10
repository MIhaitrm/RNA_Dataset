#!/usr/bin/env python

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os

# def CustomDataset(Dataset):
#     def __init__(self, annotation_file, dataset_dir):
#         self.file = pd.read_csv(annotation_file)
#         self.dir = dataset_dir
#     def __len__(self):
#         return len(self.file)

#     def __getitem__(self, idx):
#         return self.file[index][0]


# dataset = CustomDataset("pt_files/annotation_file.csv", "pt_files")
# print(dataset)


path_dat = "../pt_files"
class RNNDataset(Dataset):
    def __init__(self, annotation_file, dataset_dir):
        self.file = pd.read_csv(annotation_file)
        print(f"CSV shape: {self.file.shape}")
        self.dataset_dir = dataset_dir
        print(isinstance(self.dataset_dir, np.ndarray))
        print(isinstance(self.file, pd.DataFrame))
        # print(f"Dataset_dir shape: {self.dataset_dir.shape}")


    def __len__(self):
        return len(self.dataset_dir)

    def __getitem__(self, index):
        file_path = os.path.join(path_dat, self.file.iloc[index, 0])
        file = np.load(file_path, allow_pickle=True)
        rnn_complex = torch.Tensor(file)
        rnn_complex = torch.tensor(rnn_complex, dtype=torch.float32)
        print(rnn_complex.shape)
        return rnn_complex

print(RNNDataset(annotation_file="../pt_files/annotation_file.csv", dataset_dir=path_dat))
