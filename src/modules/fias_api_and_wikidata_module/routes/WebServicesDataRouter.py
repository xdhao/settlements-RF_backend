from datetime import datetime
from typing import List

from class_based_fastapi import Routable, get
from fastapi import Depends, HTTPException
from sqlalchemy import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from core.core_websoursces.database.database import get_session
from core.core_websoursces.models.City import City
from core.core_websoursces.models.District import District
from core.core_websoursces.models.LastAppealDate import LastAppealDate
from core.core_websoursces.models.Region import Region
from modules.fias_api_and_wikidata_module.repository.WebServicesRep import WebServicesRepository, CityPresentation, \
    DistrictPresentation
from modules.fias_api_and_wikidata_module.schemas.BasicSettlementsObjects import RegionView, DistrictView, CityView, \
    LatestDateView, Region as ViewReg


class WebServicesDataRouter(Routable):
    BASE_TEMPLATE_PATH = '/{module}/v{version}/{user_path}'
    NAME_MODULE = 'webservices_data'
    db: AsyncSession = Depends(get_session)

    def __init__(self):
        self.repository = WebServicesRepository(connection=self.db)

    @get("get-regions-with-childs", response_model=List[RegionView])
    async def get_regions_with_childs(self):
        regs = (await self.db.execute(select(Region))).scalars().all()
        reg_ids = list(map(lambda x: x.id, regs))

        districts = (await self.db.execute(select(District).filter(District.region_id.in_(reg_ids)))).scalars().all()
        cities = (await self.db.execute(select(City).filter(City.region_id.in_(reg_ids)))).scalars().all()

        districts = [DistrictView.from_model(x, cities) for x in districts]
        return [RegionView.from_model(model=x, cities=cities, districts=districts) for x in regs]

    @get("get-districts", response_model=List[DistrictView])
    async def get_districts(self):
        districts_db = (await self.db.execute(select(Region))).scalars().all()
        dis_ids = list(map(lambda x: x.id, districts_db))

        cities = (await self.db.execute(select(City).filter(City.district_id.in_(dis_ids)))).scalars().all()

        return [DistrictView.from_model(x, cities) for x in districts_db]

    @get("get-cities", response_model=List[CityView])
    async def get_cities(self):
        return (await self.db.execute(select(City))).scalars().all()


class WebServicesDataRouterV2(Routable):
    BASE_TEMPLATE_PATH = '/{module}/v{version}/{user_path}'
    NAME_MODULE = 'webservices_data'
    db: AsyncSession = Depends(get_session)

    def __init__(self):
        self.repository = WebServicesRepository(connection=self.db)

    @get("get-last-appeal-date", response_model=LatestDateView)
    async def get_last_appeal_date(self):
        return (await self.db.execute(select(LastAppealDate).order_by(desc(LastAppealDate.date)))).scalars().first()

    @get("get-cities-by-region/{id}", response_model=List[CityPresentation])
    async def get_cities_by_region(self, id: int):
        res = await self.repository.get_cities_by_region_id(id)
        if res is None:
            raise HTTPException(
                status_code=404, detail="Нет данных"
            )
        return res

    @get("get-districts-by-region/{id}", response_model=List[DistrictPresentation])
    async def get_districts_by_region(self, id: int):
        res = await self.repository.get_districts_by_region_id(id)
        if res is None:
            raise HTTPException(
                status_code=404, detail="Нет данных"
            )
        return res

    @get("get-regions-without-childs", response_model=List[ViewReg])
    async def get_regions_without_childs(self):
        return await self.repository.get_regions_without_childs()
