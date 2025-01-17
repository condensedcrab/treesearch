# treesearch
Tree recognition via satellite imagery to answer a series of questions on [my blog](https://david.barbalas.net/jekyll/update/2025/01/06/palm1.html) - how many palm trees are there really in Thousand Palms, CA?


# Getting started
To run this project, you will need use a secrets manager to encode your Google maps API key `GMAP_API_KEY` and a Roboflow API key `ROBOFLOW_API`. Please make sure that they are not committed to Github! 

Get started by building the .venv with pip from the requirements file. 
```
pip install -r requirements.txt

```

Next, to grab a grid of satellite imagery from Google Maps that I used for my writeup, please run `get_imgs.py` to generate the grid of images. Google Maps imagery runs about $2/1000 API requests, so a 50x50 grid should come out to $5. I would use caution if generating a grid of other regions on sizes more than 100x100. 

# Training the Model
All of the steps to take a pre-trained YOLOv11 model and use a custom dataset are in `training.py`. The model outputs are also available at `models/runs/detect/palms_search/weights/` if you do not have the local resources for training. 

I had to use YOLOv11-nano due to memory constraints on my GPU on my personal workstation.
