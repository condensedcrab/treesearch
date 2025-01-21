import cv2
import supervision as sv
import glob
import pandas as pd
from ultralytics import YOLO

df = pd.DataFrame([])

model = YOLO(
    "models/runs/detect/palms_search/weights/best.pt"
)  # load a partially trained model
img_files = glob.glob(
    "data/thousand_palms_640x640_z20_50x50/*.png"
)
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
            result.save(filename="result.png")  # save to disk

# save the outputs to process later
df.to_csv("palmsearch_model_output.csv")