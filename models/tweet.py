from typing import Optional

from pydantic import BaseModel, PositiveInt


class Tweet(BaseModel):
    id: Optional[PositiveInt] 
    text: str 
    positive: int = 0 
    negative: int = 0 

