from fastapi import FastAPI
from selenium import webdriver



app = FastAPI()

@app.post("/run-the-spy-bot")
def run_the_spy_bot():
    return "ok"