from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, Response, HTTPException
import logging

from models.session import Session
from services import auth

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/init")
async def init_session(
    response: Response,
    session_data: Session = Depends(auth.cookie_handler)
):
    if session_data and isinstance(session_data, Session):
        return {"status": "Session already exists", "user_id": str(session_data.user_id)}
    
    user_id = str(uuid4())
    session_id = uuid4()
    new_session = Session(user_id=user_id)
    await auth.backend.create(session_id, new_session)
    auth.cookie_handler.attach_to_response(response, session_id)

    return {"status": "Session initialized", "user_id": user_id}

@router.get("/me")
async def get_session_data(
    session_data: Session = Depends(auth.verifier)
):
    if session_data:
        print(f"Retrieved session data: {session_data}")
    else:
        print(f"No valid session data found: {session_data}")
    if not session_data:
        raise HTTPException(status_code=403, detail="No valid session found")
   
    return session_data

@router.post("/clear")
async def clear_session(
    reponse: Response,
    session_data: Session = Depends(auth.verifier)
):
    if not session_data:
        return {"status": "No session to clear"}
    
    await auth.backend.delete(session_data.user_id)
    auth.cookie_handler.delete_from_response(reponse)

    return {"status": "Session cleared"}