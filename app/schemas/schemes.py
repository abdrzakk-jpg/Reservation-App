
from datetime import datetime
from pydantic import BaseModel, Field


class ApptScheme(BaseModel):
    username: str
    phone_number: str = Field(
        min_length=10,
        max_length=13,
        pattern=r"^(\+213|0)(5|6|7)\d{8}$" # support numbers of (oredoo, mobilis, djezy)
    )
    appt_at: datetime

    class Config:
        from_attributes = True


class ApptResScheme(ApptScheme):
    id: int
    sent: bool = False


class UpdateApptScheme(BaseModel): 
    username: str
    phone_number: str = Field(
        min_length=10,
        max_length=13,
        pattern=r"^(\+213|0)(5|6|7)\d{8}$" # support numbers of (oredoo, mobilis, djezy)
    )
    appt_at: datetime