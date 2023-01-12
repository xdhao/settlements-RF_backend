import uuid
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
import math

from core.core_xlsx_parser.models.AutonomicDistrict import AutonomicDistrict
from core.core_xlsx_parser.models.Country import Country
from core.core_xlsx_parser.models.FederalDistrict import FederalDistrict
from core.core_xlsx_parser.models.LocalSubject import LocalSubject
from core.core_xlsx_parser.models.People import People
from core.core_xlsx_parser.models.SomeRegion import SomeRegion
from modules.excel_data_module.schemas.view_models import PopulationView, CountryView, PeopleView, federal_DistrictView, \
    SomeRegionView, AutDisView, LocalObjView, LocalObjectsSummary, TypeMediumValueView, MediumPercMan, MediumRuralUrban


def true_round(number, ndigits=0):
    z = 10 ** ndigits
    return math.ceil(number * z) / z


class ExcelDataRepository:
    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def get_countries(self):
        countries = (
            await self.connection.execute(select(Country).options(joinedload(Country.population_obj)))).scalars().all()
        people = (await self.connection.execute(select(People))).scalars().all()
        res = []
        for country in countries:
            ur, ru = (None for _ in range(2))
            if list(filter(lambda x: x.guid == country.population_obj.urban_people, people)):
                ur = PeopleView(
                    **list(filter(lambda x: x.guid == country.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == country.population_obj.rural_people, people)):
                ru = PeopleView(
                    **list(filter(lambda x: x.guid == country.population_obj.rural_people, people))[0].dict())
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
                ur = PeopleView(
                    **list(filter(lambda x: x.guid == federal.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == federal.population_obj.rural_people, people)):
                ru = PeopleView(
                    **list(filter(lambda x: x.guid == federal.population_obj.rural_people, people))[0].dict())
            pop = PopulationView(urban_people=ur, rural_people=ru)
            res.append(federal_DistrictView(guid=federal.guid, name=federal.name, population=pop,
                                            country=federal.country_obj.name))
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
                ur = PeopleView(
                    **list(filter(lambda x: x.guid == region.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == region.population_obj.rural_people, people)):
                ru = PeopleView(
                    **list(filter(lambda x: x.guid == region.population_obj.rural_people, people))[0].dict())
            pop = PopulationView(urban_people=ur, rural_people=ru)
            res.append(
                SomeRegionView(guid=region.guid, name=region.name, population=pop, district=region.district_obj.name))
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
        locals = (await self.connection.execute(select(LocalSubject).filter(LocalSubject.region_guid == id)
                                                .options(joinedload(LocalSubject.people_obj),
                                                         joinedload(LocalSubject.region_obj)))).scalars().all()
        res = []
        count_city, count_pgt, count_p, count_selo = (0 for _ in range(4))
        for local in locals:
            pop = PeopleView(**local.people_obj.dict())
            if local.type == 'город':
                count_city += 1
            if local.type == 'поселок городского типа':
                count_pgt += 1
            if local.type == 'поселок':
                count_p += 1
            if local.type == 'село':
                count_selo += 1
            object = LocalObjView(guid=local.guid, name=local.name, people=pop, region=local.region_obj.name,
                                  type=local.type)
            for name, val in object.people.dict().items():
                if name in ['all', 'man', 'woman', 'man_perc', 'woman_perc'] and val is not None and math.isnan(val):
                    setattr(object.people, name, None)
            res.append(object)
        result = LocalObjectsSummary(count_city=count_city, count_pgt=count_pgt,
                                     count_p=count_p, count_selo=count_selo, objects=res)
        return result

    async def get_types_medium_value(self):
        locals = (await self.connection.execute(select(LocalSubject))).scalars().all()
        regs = (await self.connection.execute(select(SomeRegion))).scalars().all()
        len_regs = len(regs)
        count_city, count_pgt, count_p, count_selo = (0 for _ in range(4))
        for local in locals:
            if local.type == 'город':
                count_city += 1
            if local.type == 'поселок городского типа':
                count_pgt += 1
            if local.type == 'поселок':
                count_p += 1
            if local.type == 'село':
                count_selo += 1

        result = TypeMediumValueView(medium_city=math.ceil(count_city / len_regs),
                                     medium_pgt=math.ceil(count_pgt / len_regs),
                                     medium_p=math.ceil(count_p / len_regs),
                                     medium_selo=math.ceil(count_selo / len_regs))
        return result

    async def get_medium_people_perc(self):
        people = (await self.connection.execute(select(People))).scalars().all()
        federals = (await self.connection.execute(select(FederalDistrict)
                                                  .options(joinedload(FederalDistrict.population_obj), joinedload(
            FederalDistrict.country_obj)))).scalars().all()
        sum_ru_man_perc = 0
        sum_ru_woman_perc = 0
        sum_ur_man_perc = 0
        sum_ur_woman_perc = 0
        for federal in federals:
            ur, ru = (None for _ in range(2))
            if list(filter(lambda x: x.guid == federal.population_obj.urban_people, people)):
                ur = PeopleView(
                    **list(filter(lambda x: x.guid == federal.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == federal.population_obj.rural_people, people)):
                ru = PeopleView(
                    **list(filter(lambda x: x.guid == federal.population_obj.rural_people, people))[0].dict())
            sum_ru_man_perc += ru.man_perc
            sum_ru_woman_perc += ru.woman_perc
            sum_ur_man_perc += ur.man_perc
            sum_ur_woman_perc += ur.woman_perc
        res = MediumPercMan(medium_ur_man=true_round(sum_ur_man_perc/len(federals), 3), medium_ur_woman=true_round(sum_ur_woman_perc/len(federals), 3),
                            medium_ru_man=true_round(sum_ru_man_perc/len(federals), 3),
                            medium_ru_woman=true_round(sum_ru_woman_perc/len(federals), 3))

        return res

    async def get_perc_rural_urban(self):
        countries = (
            await self.connection.execute(select(Country).options(joinedload(Country.population_obj)))).scalars().all()
        people = (await self.connection.execute(select(People))).scalars().all()
        all_ru = 0
        all_ur = 0
        for country in countries:
            ur, ru = (None for _ in range(2))
            if list(filter(lambda x: x.guid == country.population_obj.urban_people, people)):
                ur = PeopleView(
                    **list(filter(lambda x: x.guid == country.population_obj.urban_people, people))[0].dict())
            if list(filter(lambda x: x.guid == country.population_obj.rural_people, people)):
                ru = PeopleView(
                    **list(filter(lambda x: x.guid == country.population_obj.rural_people, people))[0].dict())
            all_ur += ur.all
            all_ru += ru.all
        return MediumRuralUrban(medium_urban=true_round((all_ur/(all_ru+all_ur)*100), 2),
                                medium_rural=true_round((all_ru/(all_ur+all_ru)*100), 2))

