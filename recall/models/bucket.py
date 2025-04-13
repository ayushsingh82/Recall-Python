from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime

class Bucket(BaseModel):
    """Model representing a Recall Network bucket."""
    id: str
    name: str
    owner: str
    created_at: datetime
    updated_at: datetime 