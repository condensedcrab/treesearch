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

# %%


ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API") # add Roboflow api to .env file in main git repo
rf = Roboflow(api_key=ROBOFLOW_API_KEY)

workspace = rf.workspace("treesearch")
project = workspace.project("palms-nfvyz")
version = project.version(3)
dataset = version.download("yolov11")
# %%
