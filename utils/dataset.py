import numpy as np
import os
from PIL import Image
import json
import torch
from torchvision import transforms
from torch.utils.data import Dataset

from utils.prep_utils import (
    projectPoints,
    vector_to_heatmaps,
    RAW_IMG_SIZE,
    MODEL_IMG_SIZE,
    DATASET_MEANS,
    DATASET_STDS,
)


class FreiHAND(Dataset):
    def __init__(self, config, set_type="train"):
        self.device = config["device"]
        self.image_dir = os.path.join(config["data_dir"], "training/rgb")
        self.image_names = np.sort(os.listdir(self.image_dir))
        print('image_names: ' + str(len(self.image_names)))
        
        fn_K_matrix = os.path.join(config["data_dir"], "training_K.json")
        with open(fn_K_matrix, "r") as f:
            self.K_matrix = np.array(json.load(f))
            self.K_matrix = np.append(self.K_matrix, self.K_matrix, axis = 0)
            self.K_matrix = np.append(self.K_matrix, self.K_matrix, axis = 0)
            print('K_matrix: ' + str(len(self.K_matrix)))

        fn_anno = os.path.join(config["data_dir"], "training_xyz.json")
        with open(fn_anno, "r") as f:
            self.anno = np.array(json.load(f))
            self.anno = np.append(self.anno, self.anno, axis = 0)
            self.anno = np.append(self.anno, self.anno, axis = 0)
            print('anno: ' + str(len(self.anno)))
        if set_type == "train":
            n_start = 0
            n_end = 104192
        elif set_type == "val":
            n_start = 104192
            n_end = 123728
        else:
            n_start = 123728
            n_end = len(self.anno)
            
        #n_start = 0
        #n_end = 4

        self.image_names = self.image_names[n_start:n_end]
        self.K_matrix = self.K_matrix[n_start:n_end]
        self.anno = self.anno[n_start:n_end]

        self.image_raw_transform = transforms.ToTensor()
        self.image_transform = transforms.Compose(
            [
                transforms.Resize(MODEL_IMG_SIZE),
                transforms.ToTensor(),
                transforms.Normalize(mean=DATASET_MEANS, std=DATASET_STDS),
            ]
        )

    def __len__(self):
        return len(self.anno)

    def __getitem__(self, idx):
        image_name = self.image_names[idx]
        image_raw = Image.open(os.path.join(self.image_dir, image_name))
        image = self.image_transform(image_raw)
        image_raw = self.image_raw_transform(image_raw)
        
        keypoints = projectPoints(self.anno[idx], self.K_matrix[idx])
        keypoints = keypoints / RAW_IMG_SIZE
        heatmaps = vector_to_heatmaps(keypoints)
        keypoints = torch.from_numpy(keypoints)
        heatmaps = torch.from_numpy(np.float32(heatmaps))

        return {
            "image": image,
            "keypoints": keypoints,
            "heatmaps": heatmaps,
            "image_name": image_name,
            "image_raw": image_raw,
        }
