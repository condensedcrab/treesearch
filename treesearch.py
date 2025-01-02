# %%

import os
from dotenv import load_dotenv
import requests

load_dotenv()
MY_API = os.getenv("GMAP_API_KEY")

class SatImg():
    
    def __init__(self):
        self.data = []
        self.session_token = ""


    def get_session_url(self):
        create_session_url = "https://tile.googleapis.com/v1/createSession"

        payload = {
            "mapType": "satellite",
            "language": "en-US",
            "region": "US",
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            create_session_url, json=payload, headers=headers, params={"key": MY_API}
        )

        if response.status_code == 200:
            self.sesion_token = response.json().get("session")
            print("Session token:", session_token)
        else:
            print("Failed to create session:", response.text)

def get_tile()


# %%

get_session_url(MY_API)
