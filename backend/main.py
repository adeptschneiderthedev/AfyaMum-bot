from fastapi import FastAPI
from pydantic import BaseModel
from utils import generate_description
from dotenv import load_dotenv, find_dotenv
from utils import generate_response

_ = load_dotenv(find_dotenv())

app = FastAPI()

_ = load_dotenv(find_dotenv())


class Prompt(BaseModel):
    prompt: str


@app.post("/afyamumbot/generate/")
async def generate(prompt: Prompt):
    description = generate_response(prompt.prompt)
    return description