from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

from models import PyObjectId

class GuestModal(BaseModel):
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  platform: Optional[str] = None
  time_visit: Optional[datetime] = None
  ip_address: Optional[str] = None
  browser_info: Optional[str] = None
  country: Optional[str] = None
  language: Optional[str] = None
  referral_source: Optional[str] = None

  model_config = ConfigDict(
    populate_by_name=True,
    protected_namespaces=('guest_info_model_'),
    arbitrary_types_allowed=True,
    json_schema_extra={
      "example": {
        "platform": "Web",
        "time_visit": "2023-01-01T12:00:00",
        "ip_address": "192.168.1.1",
        "browser_info": "Chrome",
        "country": "US",
        "language": "English",
        "referral_source": "Google"
      }
    }
  )
