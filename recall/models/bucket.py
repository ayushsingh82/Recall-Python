# This file defines the data model for buckets
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime

class Bucket(BaseModel):
    """
    Model representing a Recall Network bucket.
    
    This Pydantic model provides type validation and serialization
    for bucket data returned from the API.
    
    Attributes:
        id: Unique identifier for the bucket
        name: Human-readable name of the bucket
        owner: Address of the bucket owner
        created_at: Timestamp when the bucket was created
        updated_at: Timestamp when the bucket was last updated
    """
    id: str
    name: str
    owner: str
    created_at: datetime
    updated_at: datetime 