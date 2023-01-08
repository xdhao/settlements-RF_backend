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


class District(BaseModel):
    id: int
    region_id: Optional[int] = None
    name: str
    cities: Optional[List[City]]
    type: str


class Region(BaseModel):
    id: int
    name: str
    districts: Optional[List[District]]
    cities: Optional[List[City]]
    type: str

