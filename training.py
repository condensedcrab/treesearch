# %%
# following instructions from: https://blog.roboflow.com/yolov11-how-to-train-custom-data/
# and Google colab notebook: https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolo11-object-detection-on-custom-dataset.ipynb?ref=blog.roboflow.com#scrollTo=1nOnTQynZfeA

import ultralytics
from PIL import Image
from roboflow import Roboflow
from dotenv import load_dotenv
import os


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
# !yolo train model=yolo11n.pt data=palms-3/data.yml epochs=3 imgsz=640

# %% run YOLO model in Python
from ultralytics import YOLO

# Create a new YOLO model from scratch
model = YOLO("yolo11n.yaml")

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo11n.pt")

# Train the model using the 'coco8.yaml' dataset for 3 epochs
results = model.train(data=f"{dataset.location}/data.yaml", epochs=3)

# Evaluate the model's performance on the validation set
results = model.val()
