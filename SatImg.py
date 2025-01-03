# %%

import os
from dotenv import load_dotenv
import requests
import numpy as np
import math
import json


load_dotenv()


class SatImg:

    def __init__(self):
        self.data = []
        self.session_token = ""

        self.MY_GMAP_API = os.getenv("GMAP_API_KEY")
        self.get_session_token()

    def get_session_token(self):
        create_session_url = "https://tile.googleapis.com/v1/createSession"

        payload = {
            "mapType": "satellite",
            "language": "en-US",
            "region": "US",
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            create_session_url,
            json=payload,
            headers=headers,
            params={"key": self.MY_GMAP_API},
        )

        if response.status_code == 200:
            session_token = response.json().get("session")
            print("Session token:", session_token)
            self.session_token = session_token
        else:
            print("Failed to create session:", response.text)
            raise ValueError

    def get_2d_tile(self, z, x, y):

        input_url = f"https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}?session={self.session_token}&key={self.MY_GMAP_API}"

        r = requests.get(input_url)

        if r.status_code != 200:
            print(r.content)
        filename = f"data/x_{x}_y_{y}_z_{z}.png"
        with open(filename, "wb") as file:
            file.write(r.content)

    def convertLatLongToPoint(self, latitude, longitude, tile_size):  # TODO
        # ref: https://gis.stackexchange.com/questions/7430/what-ratio-scales-do-google-maps-zoom-levels-correspond-to
        # ref: https://groups.google.com/g/google-maps-js-api-v3/c/
        # ref: https://developers.google.com/maps/documentation/javascript/examples/map-coordinates
        siny = np.sin(latitude * np.pi / 180)
        # these are the world coordinates in the language of gmaps
        x = int(tile_size * (longitude / 360 + 0.5))
        y = int(tile_size * (0.5 - np.log((1 + siny) / (1 - siny)) / (4 * np.pi)))

        return x, y

    def convertLatLongToTileCoord(self, latitude, longitude, tile_size, zoom):
        point = self.convertLatLongToPoint(latitude, longitude, tile_size)
        scale = 2**zoom

        x = int(np.floor(point[0] * scale / tile_size))
        y = int(np.floor(point[1] * scale / tile_size))

        # pixelCoordinate = worldCoordinate * 2zoomLevel
        return x, y

    def get_static_map(self, lat, long, zoom):

        request_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{long}&format=png&zoom={zoom}&size=600x600&maptype=satellite&key={self.MY_GMAP_API}"
        r = requests.get(request_url)
        print(f"Response status is: {r.status_code}")
        filename = f"data/lat_{lat}_long_{long}_zoom_{zoom}.png"
        with open(filename, "wb") as file:
            file.write(r.content)

    def get_location_grid(self, name_string):
        # name string should be format like: "Mountain View, CA", or "Thousand Palms, CA"
        request_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={name_string}&key={self.MY_GMAP_API}"

        r = requests.get(request_url)
        output = json.loads(r.content.decode("utf-8"))

        return


# %%
zoom_lvl = 5
s = SatImg()
# s.get_static_map(33.821179, -116.394663, 18)
# s.get_static_map(33.813278287410995, -116.38493583152912, 18)
# s.get_location_grid("Thousand Palms, CA")

output = s.convertLatLongToTileCoord(
    33.813278287410995, -116.38493583152912, 256, zoom_lvl
)

for i in range(0, 10):
    s.get_2d_tile(zoom_lvl, output[0] + i, output[1])

# %%

s.convertLatLongToPoint(41.85, -87.65, 256)
s.convertLatLongToTileCoord(41.85, -87.65, 256, 19)
