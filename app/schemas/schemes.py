
from datetime import datetime, timezone
from pydantic import BaseModel, Field


# Expected appointment forms
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
    reminde_date: datetime = datetime.now(timezone.utc)
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