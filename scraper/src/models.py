from pydantic import BaseModel
from typing import List


class AdvertModel(BaseModel):
    url: str
    title: str
    price: str
    address: str
    amount_rooms: str
    description: str
    image_urls: List[str] = []
