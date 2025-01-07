# %%
# following instructions from: https://blog.roboflow.com/yolov11-how-to-train-custom-data/
# and Google colab notebook: https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolo11-object-detection-on-custom-dataset.ipynb?ref=blog.roboflow.com#scrollTo=1nOnTQynZfeA

import ultralytics
from PIL import Image
from roboflow import Roboflow
from dotenv import load_dotenv
import os

%load_ext tensorboard
%tensorboard --logdir /home/david/git/yolo11/runs

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
from ultralytics import YOLO

# # Create a new YOLO model from scratch
# model = YOLO("yolo11n.yaml")

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo11n.pt")
# model = YOLO("/home/david/git/yolo11/runs/detect/train15_200/weights/last.pt")  # load a partially trained model

# Train the model using data from Roboflow 
results = model.train(data=f"{dataset.location}/data.yaml", epochs=5000,name="palms_v3",patience=200)
# results = model.train(data=f"{dataset.location}/data.yaml", epochs=5000, resume=True,patience=100)
# Evaluate the model's performance on the validation set
results = model.val()


