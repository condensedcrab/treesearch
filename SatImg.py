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
        self.TILE_SIZE = 256  # pixels

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

    def convertLatLongToWorldCoord(self, latitude, longitude):  # TODO
        TILE_SIZE = self.TILE_SIZE

        # ref: https://gis.stackexchange.com/questions/7430/what-ratio-scales-do-google-maps-zoom-levels-correspond-to
        # ref: https://groups.google.com/g/google-maps-js-api-v3/c/
        # ref: https://developers.google.com/maps/documentation/javascript/examples/map-coordinates
        siny = np.sin(latitude * np.pi / 180)
        # mercator = -np.log(np.tan(0.25 + latitude / 360) * np.pi)
        # these are the world coordinates in the language of gmaps
        world_x = TILE_SIZE * (longitude / 360 + 0.5)
        world_y = TILE_SIZE * (0.5 - np.log((1 + siny) / (1 - siny)) / (4 * np.pi))
        # y = TILE_SIZE / 2 * (1 + mercator / np.pi)

        return world_x, world_y

    def convertLatLongToTileCoord(self, latitude, longitude, zoom):
        TILE_SIZE = self.TILE_SIZE
        point = self.convertLatLongToWorldCoord(latitude, longitude)
        scale = 2**zoom

        tile_x = int(np.floor(point[0] * scale / TILE_SIZE))
        tile_y = int(np.floor(point[1] * scale / TILE_SIZE))

        # pixelCoordinate = worldCoordinate * 2zoomLevel
        return tile_x, tile_y

    def convertToPixelCoord(self, lat, long, zoom):
        TILE_SIZE = self.TILE_SIZE
        world_coord = self.convertLatLongToWorldCoord(lat, long)

        scale = 2**zoom
        pixel_x = np.round(world_coord[0] * scale)
        pixel_y = np.round(world_coord[1] * scale)

        return pixel_x, pixel_y

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
zoom_lvl = 10
s = SatImg()
# s.get_static_map(33.821179, -116.394663, 18)
# s.get_static_map(33.813278287410995, -116.38493583152912, 18)
# s.get_location_grid("Thousand Palms, CA")

output = s.convertLatLongToTileCoord(41.85, -87.65, zoom_lvl)
output = s.convertToPixelCoord(41.85, -87.65, zoom_lvl)

# for i in range(0, 4):
#     s.get_2d_tile(zoom_lvl, output[0] + i, output[1])

# %%

s.convertLatLongToPoint(41.85, -87.65)
s.convertLatLongToTileCoord(41.85, -87.65, 19)
