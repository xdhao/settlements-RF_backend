from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.core_websoursces.models.City import City
from core.core_websoursces.models.District import District
from core.core_websoursces.models.Region import Region


class CityPresentation(BaseModel):
    id: int
    region: Optional[str] = None
    district: Optional[str] = None
    name: str
    people: Optional[int] = None
    area: Optional[float] = None
    head: Optional[str] = None
    type: str

    @staticmethod
    def from_model(model, regs, dis):
        region, district = (None for _ in range(2))
        if list(filter(lambda x: x.id == model.region_id, regs)):
            region = list(filter(lambda x: x.id == model.region_id, regs))[0].name
        if list(filter(lambda x: x.id == model.district_id, dis)):
            district = list(filter(lambda x: x.id == model.district_id, dis))[0].name
        return CityPresentation(id=model.id,
                                region=region,
                                district=district,
                                name=model.name,
                                people=model.people,
                                area=model.area,
                                head=model.head,
                                type=model.type)


class DistrictPresentation(BaseModel):
    id: int
    region: Optional[str] = None
    name: str
    type: str

    @staticmethod
    def from_model(model, regs):
        region, district = (None for _ in range(2))
        if list(filter(lambda x: x.id == model.region_id, regs)):
            region = list(filter(lambda x: x.id == model.region_id, regs))[0].name
        return DistrictPresentation(id=model.id,
                                    region=region,
                                    name=model.name,
                                    type=model.type)


class WebServicesRepository:
    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def get_regions_without_childs(self):
        return (await self.connection.execute(select(Region))).scalars().all()

    async def get_cities_by_region_id(self, region_id):
        cits = (await self.connection.execute(select(City).filter(City.region_id == region_id))).scalars().all()
        dis = (await self.connection.execute(select(District))).scalars().all()
        reg = (await self.connection.execute(select(Region).filter(Region.id == region_id))).scalars().first()
        return [CityPresentation.from_model(x, [reg], dis) for x in cits]

    async def get_districts_by_region_id(self, region_id):
        dis = (await self.connection.execute(select(District).filter(District.region_id == region_id))).scalars().all()
        reg = (await self.connection.execute(select(Region).filter(Region.id == region_id))).scalars().first()
        return [DistrictPresentation.from_model(x, [reg]) for x in dis]

