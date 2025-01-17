# %%
# following instructions from: https://blog.roboflow.com/yolov11-how-to-train-custom-data/
# and Google colab notebook: https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolo11-object-detection-on-custom-dataset.ipynb?ref=blog.roboflow.com#scrollTo=1nOnTQynZfeA

import ultralytics
from PIL import Image
from roboflow import Roboflow
from dotenv import load_dotenv
import os
from ultralytics import YOLO

# %load_ext tensorboard
# %tensorboard --logdir /home/david/git/yolo11/runs

load_dotenv()
ultralytics.checks()

# %% setup roboflow data (if not already present)
ROBOFLOW_API_KEY = os.getenv(
    "ROBOFLOW_API"
)  # add Roboflow api to .env file in main git repo
rf = Roboflow(api_key=ROBOFLOW_API_KEY)

workspace = rf.workspace("treesearch")
project = workspace.project("palms-nfvyz")
version = project.version(3)
dataset = version.download("yolov11")

# %% run YOLO model in Python
flag_train = False

if flag_train:
    # Load a pretrained YOLO model (recommended for training)
    model = YOLO("yolo11n.pt")  # only nano model fits in VRAM

    # Train the model using data from Roboflow and verify against validation set
    results = model.train(
        data=f"{dataset.location}/data.yaml",
        epochs=200,
        resume=False,
        name="palms_search",
    )
    results = model.val()

# %%
# using ultralytics docs: https://docs.ultralytics.com/modes/predict/#__tabbed_1_1
import cv2
import supervision as sv
import glob
import pandas as pd

df = pd.DataFrame([])

model = YOLO(
    "models/weights/last.pt"
)  # load a partially trained model
img_files = glob.glob(
    "data/thousand_palms_640x640_z20_50x50/*.png"
)
img_files = []
# Run batched inference on a list of images

for img in img_files:
    results = model(img)  # return a list of Results objects

    # Process results list

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
            result.save(filename="result.png")  # save to disk


df.to_csv("model_output.csv")
