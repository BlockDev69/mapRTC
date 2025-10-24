from fastapi import FastAPI
from os import environ as env

app = FastAPI()

@app.get("/")
def read_root():
    return {"details": f"Hello, World from mapRTC={env.get('MY_VARIABLE', 'default-value')}"}