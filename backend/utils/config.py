import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# API KEY PATH FROM .env
# -------------------------

KEY_PATH = os.getenv("OPENAI_API_KEY_PATH")

# -------------------------
# EXISTING PATH CONFIG
# -------------------------

DATA_DIR = "data"

TRIPS_DIR = os.path.join(DATA_DIR, "trips")

VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_db")

COLLECTION_NAME = "research_plan_memory"


os.makedirs(TRIPS_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

if KEY_PATH is None:
    raise ValueError("OPENAI_API_KEY_PATH not set in .env")

# convert relative path to absolute
if not os.path.isabs(KEY_PATH):
    BASE_DIR = os.path.dirname(__file__)
    KEY_PATH = os.path.abspath(os.path.join(BASE_DIR, KEY_PATH))


def load_openai_key():

    if not os.path.exists(KEY_PATH):
        raise FileNotFoundError(f"OpenAI key file not found: {KEY_PATH}")

    with open(KEY_PATH, "r") as f:
        return f.read().strip()


OPENAI_API_KEY = load_openai_key()


# print("OPENAI_API_KEY : \n",OPENAI_API_KEY)

