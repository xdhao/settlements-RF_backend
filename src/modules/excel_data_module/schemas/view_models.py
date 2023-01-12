import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PeopleView(BaseModel):
    all: Optional[int]
    man: Optional[int]
    woman: Optional[int]
    man_perc: Optional[float]
    woman_perc: Optional[float]


class PopulationView(BaseModel):
    urban_people: Optional[PeopleView]
    rural_people: Optional[PeopleView]


class CountryView(BaseModel):
    guid: uuid.UUID
    name: str
    population: Optional[PopulationView]

    class Config:
        orm_mode = True


class federal_DistrictView(BaseModel):
    guid: uuid.UUID
    name: str
    country: Optional[str] = None
    population: Optional[PopulationView]

    class Config:
        orm_mode = True


class SomeRegionView(BaseModel):
    guid: uuid.UUID
    name: str
    district: str
    population: Optional[PopulationView]

    class Config:
        orm_mode = True


class AutDisView(BaseModel):
    guid: uuid.UUID
    name: str
    region: str
    population: Optional[PopulationView]

    class Config:
        orm_mode = True


class LocalObjView(BaseModel):
    guid: uuid.UUID
    name: str
    region: str
    type: str
    people: Optional[PeopleView]

    class Config:
        orm_mode = True


class LocalObjectsSummary(BaseModel):
    count_city: Optional[int]
    count_pgt: Optional[int]
    count_p: Optional[int]
    count_selo: Optional[int]
    objects: Optional[List[LocalObjView]]


class TypeMediumValueView(BaseModel):
    medium_city: Optional[int]
    medium_pgt: Optional[int]
    medium_p: Optional[int]
    medium_selo: Optional[int]


class MediumPercMan(BaseModel):
    medium_ur_man: Optional[float]
    medium_ur_woman: Optional[float]
    medium_ru_man: Optional[float]
    medium_ru_woman: Optional[float]


class MediumRuralUrban(BaseModel):
    medium_urban: Optional[float]
    medium_rural: Optional[float]
