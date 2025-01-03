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
        print(f"Response status is: {r.status_code}")
        with open("output.png", "wb") as file:
            file.write(r.content)

    def convertLatLongToPoint(self, latitude, longitude, tile_size):  # TODO
        mercator = -np.log(np.tan((0.25 * latitude / 360) * np.pi))
        x = tile_size * (longitude / 360 + 0.5)
        y = tile_size / 2 * (1 + mercator / np.pi)

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

s = SatImg()
s.get_static_map(33.821179, -116.394663, 18)
s.get_static_map(33.813278287410995, -116.38493583152912, 18)
s.get_location_grid("Thousand Palms, CA")
