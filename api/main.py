from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import random

from fastapi.middleware.cors import CORSMiddleware



DATA_PATH = Path(__file__).parent.parent / "data" / "Access_to_Work_Cost_Weighted_2000.csv"
df = pd.read_csv(DATA_PATH)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)


class Profile(BaseModel):
    name: str
    condition: str
    job_role: str

@app.post("/suggest")
def suggest(profile: Profile):
    """Return 3 random supports that exist in the CSV for now."""
    # Placeholder: filter by condition & job_role _if_ you like
    choices = df["Support Provided"].sample(3).tolist()
    return {"supports": choices}
