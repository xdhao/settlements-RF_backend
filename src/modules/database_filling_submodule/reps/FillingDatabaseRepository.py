from datetime import datetime

from sqlalchemy import select
import pytz
from sqlalchemy.ext.asyncio import AsyncSession

from core.core_websoursces.models.City import City
from core.core_websoursces.models.District import District
from core.core_websoursces.models.LastAppealDate import LastAppealDate
from core.core_websoursces.models.Region import Region as WebServiceRegion

from core.core_xlsx_parser.models.AutonomicDistrict import AutonomicDistrict
from core.core_xlsx_parser.models.Country import Country
from core.core_xlsx_parser.models.FederalDistrict import FederalDistrict
from core.core_xlsx_parser.models.LocalSubject import LocalSubject
from core.core_xlsx_parser.models.People import People
from core.core_xlsx_parser.models.Population import Population
from core.core_xlsx_parser.models.SomeRegion import SomeRegion as ExcelRegion

from modules.fias_api_and_wikidata_module.scripts.settlements_data_requestor import SettlementsDataRequestor
from modules.parsing_from_xlsx.XlsxSettlementsParser import XlsxSettlementsParser


class FillingDatabaseRepository:
    def __init__(self, connection_1: AsyncSession, connection_2: AsyncSession):
        self.connection_1 = connection_1
        self.connection_2 = connection_2
        self.WebServicesDataClass = SettlementsDataRequestor()
        self.ExcelDataClass = XlsxSettlementsParser()

    async def fill_with_data_from_webservices(self):

        # ИДЕНТИФИКАТОРЫ ЗАПИСЕЙ, СУЩЕСТВУЮЩИХ В БД
        db_regions = (await self.connection_1.execute(select(WebServiceRegion))).scalars().all()
        reg_ids = list(map(lambda x: x.id, db_regions))

        db_districts = (await self.connection_1.execute(select(District))).scalars().all()
        dis_ids = list(map(lambda x: x.id, db_districts))

        db_cities = (await self.connection_1.execute(select(City))).scalars().all()
        cit_ids = list(map(lambda x: x.id, db_cities))

        # данные, спаршенные из внешних сервисов, которых нет в бд
        appended_regions = list(filter(lambda x: x.id not in reg_ids, self.WebServicesDataClass.regions))
        appended_districts = list(filter(lambda x: x.id not in dis_ids, self.WebServicesDataClass.districts))
        appended_cities = list(filter(lambda x: x.id not in cit_ids, self.WebServicesDataClass.cities))

        # ДОБАВЛЯЕМ НОВЫЕ ДАННЫЕ В БД
        self.connection_1.add_all([WebServiceRegion(**x.dict()) for x in appended_regions])
        self.connection_1.add_all([District(**x.dict()) for x in appended_districts])
        self.connection_1.add_all([City(**x.dict()) for x in appended_cities])

        # обновляем дату последнего обращения
        appeal_date = (await self.connection_1.execute(select(LastAppealDate))).scalars().first()
        if appeal_date:
            appeal_date.date = datetime.now(tz=pytz.UTC)
        else:
            self.connection_1.add(LastAppealDate(date=datetime.now(tz=pytz.UTC)))
        await self.connection_1.commit()

        return 'данные успешно обновлены'

    async def fill_with_data_from_excel(self):

        # ИДЕНТИФИКАТОРЫ ЗАПИСЕЙ, СУЩЕСТВУЮЩИХ В БД
        db_countries = (await self.connection_2.execute(select(Country))).scalars().all()
        countries_ids = list(map(lambda x: x.guid, db_countries))

        db_districts = (await self.connection_2.execute(select(FederalDistrict))).scalars().all()
        dis_ids = list(map(lambda x: x.guid, db_districts))

        db_regions = (await self.connection_2.execute(select(ExcelRegion))).scalars().all()
        reg_ids = list(map(lambda x: x.guid, db_regions))

        db_au_districts = (await self.connection_2.execute(select(AutonomicDistrict))).scalars().all()
        au_districts_ids = list(map(lambda x: x.guid, db_au_districts))

        db_cities = (await self.connection_2.execute(select(LocalSubject))).scalars().all()
        cit_ids = list(map(lambda x: x.guid, db_cities))

        # добавляем данные о популяции
        self.connection_2.add_all([People(**x.__dict__) for x in self.ExcelDataClass.peoples])
        await self.connection_2.commit()

        self.connection_2.add_all([Population(**x.__dict__) for x in self.ExcelDataClass.pops])
        await self.connection_2.commit()

        # данные, спаршенные из внешних сервисов, которых нет в бд
        appended_regions = list(filter(lambda x: x.guid not in reg_ids, self.ExcelDataClass.regions))
        appended_districts = list(filter(lambda x: x.guid not in dis_ids, self.ExcelDataClass.federals))
        appended_countries = list(filter(lambda x: x.guid not in countries_ids, self.ExcelDataClass.country))
        appended_cities = list(filter(lambda x: x.guid not in cit_ids, self.ExcelDataClass.local_objects))
        appended_au_dises = list(filter(lambda x: x.guid not in au_districts_ids, self.ExcelDataClass.aut_dises))

        # ДОБАВЛЯЕМ НОВЫЕ ДАННЫЕ В БД
        self.connection_2.add_all([Country(**x.__dict__) for x in appended_countries])
        await self.connection_2.commit()

        self.connection_2.add_all([FederalDistrict(**x.__dict__) for x in appended_districts])
        await self.connection_2.commit()

        self.connection_2.add_all([ExcelRegion(**x.__dict__) for x in appended_regions])
        await self.connection_2.commit()

        self.connection_2.add_all([AutonomicDistrict(**x.__dict__) for x in appended_au_dises])
        await self.connection_2.commit()

        self.connection_2.add_all([LocalSubject(**x.__dict__) for x in appended_cities])
        await self.connection_2.commit()

        return 'данные успешно спаршены'





