from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class CityView(BaseModel):
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


class DistrictView(District):
    cities: Optional[List[CityView]]

    @staticmethod
    def from_model(model, cities):
        return DistrictView(cities=list(filter(lambda x: x.region_id == model.id, cities)), **model.dict())


class RegionView(Region):
    districts: Optional[List[DistrictView]]
    cities: Optional[List[CityView]]

    @staticmethod
    def from_model(model, cities, districts):
        return RegionView(cities=list(filter(lambda x: x.region_id == model.id, cities)),
                          districts=list(filter(lambda x: x.region_id == model.id, districts)),
                          **model.dict())


class LatestDateView(BaseModel):
    date: datetime
