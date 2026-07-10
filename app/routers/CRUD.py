from typing import List
from sqlalchemy.orm import Session
from app.models import Appt
from fastapi import Depends, status, APIRouter, HTTPException
from app.src.utils import get_db
from app.schemas.schemes import *
from rich import print
from datetime import datetime, timezone, timedelta


router = APIRouter(
    prefix='/appointments', 
)



#* get appts
# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[ApptResScheme])
@router.get("/", status_code=status.HTTP_200_OK, response_model=ApptResScheme)
def get_appts(db: Session = Depends(get_db)):

    appts = db.query(Appt).order_by(Appt.appt_at.asc()).first()
    

    # reminde_date = datetime.strptime(str(appts.appt_at), "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
    now = datetime.now(timezone.utc)

    reminde_date = now + timedelta(days=1)

    print(f"[yellow bold]We Are in: {now.strftime("%Y-%m-%d %H:%M:%S")}[/yellow bold]")
    
    print(f"[yellow bold]Reminde in: {reminde_date.replace(hour=10, minute=0).strftime("%Y-%m-%d %H:%M:%S")}[/yellow bold]")



    
    return appts


#* add appt
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApptScheme)
async def add_appt( appt: ApptScheme, db: Session = Depends(get_db) ):
    if db.query(Appt).filter( Appt.phone_number == appt.phone_number ).first():

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone Number Is Used"
        )

    created_appt = Appt(**appt.model_dump())

    db.add(created_appt)
    db.commit()
    db.refresh(created_appt)

    return created_appt
    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ApptResScheme)
async def update_appt( id: int, selectd_appt: UpdateApptScheme, db: Session = Depends(get_db)  ):

    appt_query = db.query(Appt).filter( Appt.id == id )
    current_appt = appt_query.first()

    if current_appt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    if(current_appt.phone_number != selectd_appt.phone_number):


        # recheck if given number is used   
        check_query = db.query( Appt ).filter(Appt.phone_number == selectd_appt.phone_number)
        current_number = check_query.first()


        if current_number:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Number Is Used"
        )   
        # pyrefly: ignore [bad-assignment]
        current_appt.phone_number = selectd_appt.phone_number

    appt_query.update(
        {**selectd_appt.model_dump()}, # it needs {} to work :)
        synchronize_session=False
    )
    
    db.commit()
    db.refresh(current_appt)
    return current_appt

    

    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appts(id:int ,    db: Session = Depends(get_db)):
    appt_query = db.query(Appt).filter( Appt.id == id )
    current_appt = appt_query.first()

    if current_appt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )

    db.delete(current_appt)
    db.commit()