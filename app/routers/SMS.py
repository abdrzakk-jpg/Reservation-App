
from app.services.check_logic import send_sms
from fastapi import APIRouter, HTTPException
from app.schemas.schemes import *
from app.src.dotenv_loader import ip

router = APIRouter(
    prefix='/sms', 
)
#* check SMS-Gateaway connection 
@router.get("/gateaway-check")
async def check() :
    gate_status = send_sms("0612345678", "Are You Alive ?", ip)
    print(gate_status)
    if gate_status is True:  return 200
    
    raise HTTPException(
        status_code = 503,
        detail="SMS-Gateaway Unreachable"
    )   