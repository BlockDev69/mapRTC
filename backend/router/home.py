from fastapi import APIRouter
from os import environ as env

router = APIRouter(prefix='/home', tags=['home'])

@router.get("/")
def read_root():
    return {"details": f"Hello, World from mapRTC={env.get('MY_VARIABLE', 'default-value')}"}