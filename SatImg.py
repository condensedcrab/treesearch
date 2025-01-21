# %%

import os
from dotenv import load_dotenv
import requests
import numpy as np
import math
import json
import glob


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
        # gets tile (not pixel)

        # verify that x and y are ints
        x = int(x)
        y = int(y)

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
        world_coord = self.convertLatLongToWorldCoord(lat, long)

        scale = 2**zoom
        pixel_x = int(np.round(world_coord[0] * scale))
        pixel_y = int(np.round(world_coord[1] * scale))

        return pixel_x, pixel_y

    def get_static_map(self, lat, long, zoom,file_path="data/"):
        flag_cached = False
        filename = f"{file_path}/lat_{lat:.6f}_long_{long:.6f}_zoom_{zoom}.png"

        scale = 1
        size = "640x640"

        # check if file is cached
        prev_files = glob.glob("data/*.png")
        for imgs in prev_files:
            if filename in imgs:
                print("Image already cached")
                flag_cached = True
                
        if flag_cached:
            return

        request_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{long}&format=png&zoom={zoom}&scale={scale}&size={size}&maptype=satellite&key={self.MY_GMAP_API}"
        r = requests.get(request_url)
        # print(f"Response status is: {r.status_code}")

        with open(filename, "wb") as file:
            file.write(r.content)

    def generate_location_grid(self, name_string, zoom_level=12):
        # name string should be format like: "Mountain View, CA", or "Thousand Palms, CA"
        request_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={name_string}&key={self.MY_GMAP_API}"

        r = requests.get(request_url)
        output = json.loads(r.content.decode("utf-8"))

        # grab bounds from json structure
        grid_start = output["results"][0]["geometry"]["bounds"]["southwest"]
        grid_end = output["results"][0]["geometry"]["bounds"]["northeast"]

        # grab the tile locations to generate grid
        [x1, y1] = self.convertLatLongToTileCoord(
            grid_start["lat"], grid_start["lng"], zoom_level
        )
        [x2, y2] = self.convertLatLongToTileCoord(
            grid_end["lat"], grid_end["lng"], zoom_level
        )

        # should be positive values for length
        len_x = x2 - x1
        len_y = y1 - y2

        # now construct the grid from (x1,y1) to (x2,y2)
        grid_list = np.zeros((len_x * len_y, 2))

        if grid_list.shape[0] > 2500:
            raise ValueError("Too many tiles requested")

        counter = 0
        for idx_x in range(x1, x2):
            for idx_y in range(y1, y2, -1):
                grid_list[counter, :] = [idx_x, idx_y]
                counter += 1

        return grid_list

    def get_grid_images(self, name_string, zoom_level=12):
        max_tiles = 50
        tile_grid = self.generate_location_grid(name_string, zoom_level)

        tile_counter = 0
        for idx, tile in enumerate(tile_grid):
            self.get_2d_tile(zoom_level, tile[0], tile[1])
            print(f"Tile {idx}: {tile[0]}, {tile[1]}")

            tile_counter += 1
            if tile_counter >= max_tiles:
                raise Warning("More than 10k tiles reached, terminating.")
                break

    def get_static_grid(self, lat, long, nx, ny, zoom=20,file_path="data/"):
        
        # check if file path for ouptut images is valid
        if not os.path.isdir(file_path):
            raise ValueError(f"File path is not a valid folder. Please double check your folder and try again. Your input was: {file_path}")

        # calculated latitude and longitude spacing. 
        grid_spacing = [6.5e-4, 8e-4]

        if nx % 2 == 1:
            nx -= 1
        if ny % 2 == 1:
            ny -= 1

        counter = 0
        for x in range(-nx // 2, nx // 2):
            for y in range(-nx // 2, nx // 2):
                self.get_static_map(lat + x * grid_spacing[0], long + y * grid_spacing[1], zoom, file_path
                )
                print(
                    f"Tile: {counter}/{nx*ny}: Lat: {lat + x * grid_spacing[0]:.6f}, Long: {long + y * grid_spacing[1]:.6f}"
                )
                counter += 1

    def get_bounding_coords(self, place_name):
        # name string should be format like: "Mountain View, CA", or "Thousand Palms, CA"
        request_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={self.MY_GMAP_API}"

        r = requests.get(request_url)
        output = json.loads(r.content.decode("utf-8"))

        # grab bounds from json structure
        grid_start = output["results"][0]["geometry"]["bounds"]["southwest"]
        grid_end = output["results"][0]["geometry"]["bounds"]["northeast"]


        return [
            [grid_start["lat"], grid_start["lng"]],
            [grid_end["lat"], grid_end["lng"]],
        ]
