from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/now")
async def get_current_time():
    return {"time": datetime.utcnow().isoformat()}

DEFAULT_CONFIG = {"format": "iso"}
