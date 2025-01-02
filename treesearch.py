import os
from dotenv import load_dotenv


load_dotenv()

MY_API = os.getenv("GMAP_API_KEY")
