from typing import Optional, List
from pydantic import BaseModel


class City(BaseModel):
    id: int
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    name: str
    people: Optional[int] = None
    area: Optional[float] = None
    head: Optional[str] = None
    type: str

    class Config:
        orm_mode = True


class District(BaseModel):
    id: int
    region_id: Optional[int] = None
    name: str
    type: str

    class Config:
        orm_mode = True


class Region(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        orm_mode = True
