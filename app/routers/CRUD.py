
from app.src.utils import generate_sms_msg
from app.services.check_logic import send_sms
from app.services.logger import logger
from typing import List
from sqlalchemy.orm import Session
from app.models import Appt
from fastapi import Depends, status, APIRouter, HTTPException
from app.src.utils import get_db, now
from app.schemas.schemes import *
from datetime import timedelta
from app.src.dotenv_loader import ip

router = APIRouter(
    prefix='/appointments', 
)



#* get appointments
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ApptResScheme])
# @router.get("/", status_code=status.HTTP_200_OK, response_model=ApptResScheme)
def get_appts(db: Session = Depends(get_db)):

    appts = db.query(Appt).all()
    return appts    


#* add appointment
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApptResScheme)
async def add_appt( appt: ApptScheme, db: Session = Depends(get_db) ):
    logger.info(f"Requested Data: {appt}")
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
        


        created_appt: Appt = Appt(**appt_dict)

        # if today is not reminde date (bcoz appointment date changed) change `sent` state
        if now <= (created_appt.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):
                
                
                created_appt.sent = False # pyrefly: ignore [bad-assignment]
        # if `reminde_date` is Gone
        if now >= (created_appt.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):
            msg = generate_sms_msg(
                            
                            username=created_appt.username,# pyrefly: ignore [bad-argument-type]
                            date=created_appt.appt_at # pyrefly: ignore [bad-argument-type]
                        )
            sms_send_response = send_sms(created_appt.phone_number, msg, ip)
            if sms_send_response == -1: 
                logger.exception(f"Faild to Send SMS, rollback...")
                raise HTTPException(
                    status_code = status.HTTP_503_SERVICE_UNAVAILABLE, # error [503] is more More expressive
                    detail = "SMS-Gateaway Unreachable"
                )

            created_appt.sent = True # pyrefly: ignore [bad-assignment]

        # add appointment
        db.add(created_appt)
        db.commit()
        db.refresh(created_appt)

        logger.success(f"Appointment registred with ID: #{created_appt.id}")
        return created_appt


    except HTTPException:
        raise

    except Exception as err:        
        logger.exception(f"Faild to Registe Appointment, rollback...")
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

            current_appt.phone_number = selectd_appt.phone_number # pyrefly: ignore [bad-assignment]

        # if appointment date is changed/updated
        if (current_appt.appt_at).strftime("%Y-%m-%dT%H:%M:%S") != (selectd_appt.appt_at).strftime("%Y-%m-%dT%H:%M:%S"):

            if (current_appt.appt_at).strftime("%Y-%m-%dT%H:%M:%S") > (selectd_appt.appt_at).strftime("%Y-%m-%dT%H:%M:%S"): # prevent select gone date
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't Choose Date In The Past"
                    
            )   

            # pyrefly: ignore [bad-assignment]
            current_appt.appt_at = selectd_appt.appt_at # update appointment_date
            current_appt.reminde_date = (current_appt.appt_at - timedelta(days=1)).replace(hour=10, minute=0) # update reminde_date

            # if today is not reminde date (bcoz appointment date changed) change `sent` state
            if now <= (current_appt.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):
                current_appt.sent = False # pyrefly: ignore [bad-assignment]

        # if `reminde_date` is Gone
        if now >= (current_appt.reminde_date).strftime("%Y-%m-%dT%H:%M:%S"):
                current_appt.sent = True # pyrefly: ignore [bad-assignment]

                
        appt_query.update(
            {**selectd_appt.model_dump()}, # it needs {} to work :)
            synchronize_session=False
        )
        
        db.commit()
        db.refresh(current_appt)

        logger.info(f"[#{current_appt.id}]Appointment Updated")
        return current_appt

    except HTTPException:
        raise
    except Exception as err:
        logger.exception(f"[#{id}]Faild to Update, rollback...")
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(err)
        )

    

#* delete appointment
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appts(id:int, db: Session = Depends(get_db)):
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
        logger.info(f"[#{current_appt.id}]Appointment Deleted")
        
    except HTTPException:
        raise
    except Exception as err:
        logger.exception(f"[#{id}]Faild to Delete, rollback...")
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(err)
        )

