import uuid
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.core_xlsx_parser.models.AutonomicDistrict import AutonomicDistrict
from core.core_xlsx_parser.models.Country import Country
from core.core_xlsx_parser.models.FederalDistrict import FederalDistrict
from core.core_xlsx_parser.models.LocalSubject import LocalSubject
from core.core_xlsx_parser.models.People import People
from core.core_xlsx_parser.models.SomeRegion import SomeRegion
from modules.excel_data_module.schemas.view_models import PopulationView, CountryView, PeopleView, federal_DistrictView, \
    SomeRegionView, AutDisView, LocalObjView, LocalObjectsSummary


class ExcelDataRepository:
    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def get_countries(self):
        countries = (await self.connection.execute(select(Country).options(joinedload(Country.population_obj)))).scalars().all()
        people = (await self.connection.execute(select(People))).scalars().all()
        res = []
        for country in countries:
            ur, ru = (None for _ in range(2))
            if list(filter(lambda x: x.guid == country.population_obj.urban_people, people)):
                ur = PeopleView(**list(filter(lambda x: x.guid == country.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == country.population_obj.rural_people, people)):
                ru = PeopleView(**list(filter(lambda x: x.guid == country.population_obj.rural_people, people))[0].dict())
            pop = PopulationView(urban_people=ur, rural_people=ru)
            res.append(CountryView(guid=country.guid, name=country.name, population=pop))
        return res

    async def get_federals(self):
        people = (await self.connection.execute(select(People))).scalars().all()
        federals = (await self.connection.execute(select(FederalDistrict)
                                                  .options(joinedload(FederalDistrict.population_obj), joinedload(
                                                                                             FederalDistrict.country_obj)))).scalars().all()
        res = []
        for federal in federals:
            ur, ru = (None for _ in range(2))
            if list(filter(lambda x: x.guid == federal.population_obj.urban_people, people)):
                ur = PeopleView(**list(filter(lambda x: x.guid == federal.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == federal.population_obj.rural_people, people)):
                ru = PeopleView(**list(filter(lambda x: x.guid == federal.population_obj.rural_people, people))[0].dict())
            pop = PopulationView(urban_people=ur, rural_people=ru)
            res.append(federal_DistrictView(guid=federal.guid, name=federal.name, population=pop, country=federal.country_obj.name))
        return res

    async def get_regions(self, id: uuid.UUID):
        people = (await self.connection.execute(select(People))).scalars().all()
        regions = (await self.connection.execute(select(SomeRegion).filter(SomeRegion.district_guid == id)
                                                  .options(joinedload(SomeRegion.population_obj), joinedload(
                                                                                             SomeRegion.district_obj)))).scalars().all()
        res = []
        for region in regions:
            ur, ru = (None for _ in range(2))
            if list(filter(lambda x: x.guid == region.population_obj.urban_people, people)):
                ur = PeopleView(**list(filter(lambda x: x.guid == region.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == region.population_obj.rural_people, people)):
                ru = PeopleView(**list(filter(lambda x: x.guid == region.population_obj.rural_people, people))[0].dict())
            pop = PopulationView(urban_people=ur, rural_people=ru)
            res.append(SomeRegionView(guid=region.guid, name=region.name, population=pop, district=region.district_obj.name))
        return res

    async def get_auto_districts(self):
        people = (await self.connection.execute(select(People))).scalars().all()
        au_dises = (await self.connection.execute(select(AutonomicDistrict)
                                                  .options(joinedload(AutonomicDistrict.population_obj), joinedload(
                                                                                             AutonomicDistrict.region_obj)))).scalars().all()
        res = []
        for dis in au_dises:
            ur, ru = (None for _ in range(2))
            if list(filter(lambda x: x.guid == dis.population_obj.urban_people, people)):
                ur = PeopleView(**list(filter(lambda x: x.guid == dis.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == dis.population_obj.rural_people, people)):
                ru = PeopleView(**list(filter(lambda x: x.guid == dis.population_obj.rural_people, people))[0].dict())
            pop = PopulationView(urban_people=ur, rural_people=ru)
            res.append(AutDisView(guid=dis.guid, name=dis.name, population=pop, region=dis.region_obj.name))
        return res

    async def get_local_objects(self, id):
        locals = (await self.connection.execute(select(LocalSubject).filter(LocalSubject.region_guid==id)
                                                  .options(joinedload(LocalSubject.people_obj), joinedload(LocalSubject.region_obj)))).scalars().all()
        res = []
        sum_woman, sum_man, sum_all, count_city, count_pgt, count_p, count_selo = (0 for _ in range(7))
        for local in locals:
            pop = PeopleView(**local.people_obj.dict())
            sum_woman += pop.woman
            sum_man += pop.man
            sum_all += pop.all
            if local.type == 'город':
                count_city += 1
            if local.type == 'поселок городского типа':
                count_pgt += 1
            if local.type == 'поселок':
                count_p += 1
            if local.type == 'село':
                count_selo += 1
            res.append(LocalObjView(guid=local.guid, name=local.name, people=pop, region=local.region_obj.name, type=local.type))
        result = LocalObjectsSummary(sum_woman=sum_woman, sum_man=sum_man, sum_all=sum_all,
                                     count_city=count_city, count_pgt=count_pgt,
                                     count_p=count_p, count_selo=count_selo, objects=res)
        return result