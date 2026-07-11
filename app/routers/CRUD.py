from app.services.logger import logger
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



#* get appointment
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ApptResScheme])
# @router.get("/", status_code=status.HTTP_200_OK, response_model=ApptResScheme)
def get_appts(db: Session = Depends(get_db)):

    appts = db.query(Appt).all()
    return appts


#* add appointment
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApptResScheme)
async def add_appt( appt: ApptScheme, db: Session = Depends(get_db) ):
    try:
        if db.query(Appt).filter( Appt.phone_number == appt.phone_number ).first():

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone Number Is Used"
            )

        appt_dict = appt.model_dump() # create editable copy
        # calc reminde date ( a day before )
        reminde_date = (appt.appt_at - timedelta(days=1)).replace(hour=10, minute=0)
        appt_dict["reminde_date"] = reminde_date

        print(appt_dict)
        created_appt = Appt(**appt_dict)

        db.add(created_appt)
        db.commit()
        db.refresh(created_appt)

        return created_appt

    except Exception as err:
        db.rollback()
        logger.exception(f"Unexcpected Error")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(err)
        )
#* update appointment
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ApptResScheme)
async def update_appt( id: int, selectd_appt: UpdateApptScheme, db: Session = Depends(get_db)  ):
    try:

        appt_query = db.query(Appt).filter( Appt.id == id )
        current_appt: Appt = appt_query.first()

        if current_appt is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )
        
        if(current_appt.phone_number != selectd_appt.phone_number):


            # recheck if given number is used   
            check_query = db.query( Appt ).filter(Appt.phone_number == selectd_appt.phone_number)
            current_number = check_query.first()

            # if there are already appointment with the same number 
            if current_number:
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Number Is Used"
            )   

            current_appt.phone_number = selectd_appt.phone_number

        now = (datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%S") 

        # if appointment date is changed/updated
        if(current_appt.appt_at != selectd_appt.appt_at):

            # pyrefly: ignore [bad-assignment]
            current_appt.appt_at = selectd_appt.appt_at
            current_appt.reminde_date = (current_appt.appt_at - timedelta(days=1)).replace(hour=10, minute=0)

            # if today is not reminde date (bcoz appointment date changed) change `sent` state
            if now <= (current_appt.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):
                current_appt.sent = False

        # if `reminde_date` is Gone
        if now >= (current_appt.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):
                current_appt.sent = True

        # update
        appt_query.update(
            {**selectd_appt.model_dump()}, # it needs {} to work :)
            synchronize_session=False
        )
        
        db.commit()
        db.refresh(current_appt)


        return current_appt

    except Exception as err:
        db.rollback()
        logger.exception(f"Unexcpected Error")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(err)
        )

    

#* delete appointment
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appts(id:int ,    db: Session = Depends(get_db)):
    try:
        appt_query = db.query(Appt).filter( Appt.id == id )
        current_appt = appt_query.first()

        if current_appt is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not Found"
            )
        
        db.delete(current_appt)
        db.commit()
        
    except Exception as err:
        db.rollback()
        logger.exception(f"Unexcpected Error")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(err)
        )




#  =======================|TEST-AREA|======================= #

# @router.get("/tst", status_code=status.HTTP_200_OK, response_model=ApptResScheme | dict)
def tst(db: Session = Depends(get_db)):

    appts: Appt = db.query(Appt).order_by(Appt.reminde_date.asc()).first()


    now = (datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%S")
    send = False
    if now >= (appts.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):
        send = True

    print(now)
    print((appts.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"))


    
    return {
        "Closr Appointment": appts.appt_at,
        "Reminde At": appts.reminde_date,
        "Now": now,
        "Send": send
        }