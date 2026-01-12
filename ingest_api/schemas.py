from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Literal

class EventIn(BaseModel):
    event_id: UUID
    user_id: int
    event_type: Literal["page_view", "add_to_cart", "checkout"]
    page: str
    event_time: datetime