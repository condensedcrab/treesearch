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
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API") # add Roboflow api to .env file in main git repo
rf = Roboflow(api_key=ROBOFLOW_API_KEY)

workspace = rf.workspace("treesearch")
project = workspace.project("palms-nfvyz")
version = project.version(3)
dataset = version.download("yolov11")
# %%
# !yolo train model=yolo11n.pt data=/home/david/git/treesearch/palms-3/data.yml epochs=3 imgsz=640

# %% run YOLO model in Python


# # Create a new YOLO model from scratch
# model = YOLO("yolo11n.yaml")

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo11m.pt") # use medium model
model = YOLO("/home/david/git/yolo11/runs/detect/palms_v3/weights/last.pt")  # load a partially trained model

# Train the model using data from Roboflow 
results = model.train(data=f"{dataset.location}/data.yaml", epochs=500,resume=True,name="palms_v3",patience=100)
# results = model.train(data=f"{dataset.location}/data.yaml", epochs=5000, resume=True,patience=100)
# Evaluate the model's performance on the validation set
results = model.val()

# %% 
# using ultralytics docs: https://docs.ultralytics.com/modes/predict/#__tabbed_1_1
import cv2
import supervision as sv
import glob

model = YOLO("/home/david/git/yolo11/runs/detect/palms_v3/weights/last.pt")  # load a partially trained model

img_files = glob.glob("/home/david/git/treesearch/data/thousand_palms_640x640_z20_50x50/*.png")

# Run batched inference on a list of images
results = model(img_files[0:5],stream=True)  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.png")  # save to disk
