# %%

import os
from dotenv import load_dotenv
import requests


load_dotenv()
MY_API = os.getenv("GMAP_API_KEY")


def get_session_url(api_key):
    create_session_url = "https://tile.googleapis.com/v1/createSession"

    payload = {
        "mapType": "satellite",
        "language": "en-US",
        "region": "US",
    }

    headers = {"Content-Type": "application/json"}

    return (
        "https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}?session="
        + session_token
        + "&key="
        + api_key
    )


# %%
