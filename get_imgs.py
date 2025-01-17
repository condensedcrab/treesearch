# %%
import SatImg as si

s = si.SatImg()

# use coordinate spacing to construct grid. GMaps only goes out to 6 decimal places
s.get_static_grid(33.832183, -116.534736,4,4,file_path="data/thousand_palms_640x640_z20_50x50")

