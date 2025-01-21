# %%
# following instructions from: https://blog.roboflow.com/yolov11-how-to-train-custom-data/
# and Google colab notebook: https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolo11-object-detection-on-custom-dataset.ipynb?ref=blog.roboflow.com#scrollTo=1nOnTQynZfeA

from PIL import Image
from roboflow import Roboflow
from dotenv import load_dotenv
import os
from ultralytics import YOLO

# %load_ext tensorboard
# %tensorboard --logdir /home/david/git/yolo11/runs

load_dotenv()
# ultralytics.checks()


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

