# %% load necessary packages
# import common packages and load data

import glob
import SatImg as si
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename = "model_output.csv"

df = pd.read_csv(filename)
s = si.SatImg()

output = s.get_bounding_coords("Thousand Palms, CA")

print(output)
