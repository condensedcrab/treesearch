# %% load necessary packages
# import common packages and load data

import glob
import SatImg as si
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from ultralytics import YOLO



# using ultralytics docs: https://docs.ultralytics.com/modes/predict/#__tabbed_1_1
import cv2
import supervision as sv
import glob
import pandas as pd

df = pd.DataFrame([])

model = YOLO(
    "models/runs/detect/palms_search/weights/best.pt"
)  # load a partially trained model
img_files = glob.glob(
    "data/thousand_palms_640x640_z20_50x50/*.png"
)
output_folder = "filter_data"

# Run batched inference on a list of images in a loop since I do not have sufficient video memory to stream/batch that many images at once.
for img in img_files:
    results = model(img)  # return a list of Results objects

    # Process results list and only pull the results and metadata for images with detections
    for result in results:
        if result.boxes is not None:
            df_result = result.to_df()
            # add file name so we can get out the position
            df_result["file_name"] = img

            if len(df) == 0:
                df = df_result
            else:
                df = pd.concat([df, df_result], ignore_index=True)
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            obb = result.obb  # Oriented boxes object for OBB outputs
            result.save(filename=f"{output_folder}/result.png")  # save to disk

# save the outputs to process later
df.to_csv("palmsearch_model_output.csv")

# %% analyze the results from the grid 
filename = "palmsearch_model_output.csv"

df = pd.read_csv(filename)
s = si.SatImg()
output = s.get_bounding_coords("Thousand Palms, CA")

print(output)

# %% grab the model and get the mAP, P, R
model = YOLO(
    "/home/david/git/yolo11/runs/detect/palms_v3/weights/last.pt"
)  # load a partially trained model
results = model.val()

# %% set up formatting on the df
conf_limit = [0.1, 0.15, 0.2, 0.25, 0.5]  # >= this value only

for conf_lvl in conf_limit:
    df = pd.read_csv(filename)
    rows = df["confidence"] >= conf_lvl
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


    print(f"At conf level {conf_lvl}, palms found: {num_palms}")

# %% analyze the results for the given confidence level
conf_lvl = 0.25
df = pd.read_csv(filename)
rows = df["confidence"] >= conf_lvl
df = df[rows]

plt.figure()
plt.hist(df['confidence'],bins=20,edgecolor='black')
plt.hist(df['confidence'],bins=20,edgecolor='red',cumulative=True, density=True)


plt.xlabel("Inference Confidence")
plt.ylabel("Counts")
plt.show()



# %%
