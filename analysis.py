# %% load necessary packages
# import common packages and load data

import glob
import SatImg as si
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from ultralytics import YOLO

filename = "palmsearch_model_output.csv"

df = pd.read_csv(filename)
s = si.SatImg()
output = s.get_bounding_coords("Thousand Palms, CA")

print(output)

# grab the model and get the mAP, P, R
model = YOLO(
    "/home/david/git/yolo11/runs/detect/palms_v3/weights/last.pt"
)  # load a partially trained model
results = model.val()

# %% set up formatting on the df
conf_limit = 0.25  # >= this value only

rows = df["confidence"] >= conf_limit
df = df[rows]


num_palms = 0

for index, row in df.iterrows():
    img_filename = row["file_name"]
    coords = re.findall(r"-?\d+\.\d+", img_filename)
    coords = [float(coords[0]), float(coords[1])]

    flag_valid_lat = coords[0] >= np.min([output[0][0], output[1][0]]) and coords[
        0
    ] <= np.max([output[0][0], output[1][0]])

    flag_valid_long = coords[1] >= np.min([output[0][1], output[1][1]]) and coords[
        1
    ] <= np.max([output[0][1], output[1][1]])

    if flag_valid_lat and flag_valid_long:
        num_palms += 1


print(f"Valid palms found: {num_palms}")
