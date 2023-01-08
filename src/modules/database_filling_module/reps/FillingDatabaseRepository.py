from datetime import datetime

from sqlalchemy import select
import pytz
from core.models import City
from core.models.District import District
from core.models import LastAppealDate
from core.models import Region
from modules.data_collection_module.settlements_data_requestor import SettlementsDataRequestor
from sqlalchemy.ext.asyncio import AsyncSession


class FillingDatabaseRepository:
    def __init__(self, connection: AsyncSession):
        self.connection = connection
        self.DataClass = SettlementsDataRequestor

    async def fill_database(self):

        # ИДЕНТИФИКАТОРЫ ЗАПИСЕЙ, СУЩЕСТВУЮЩИХ В БД
        db_regions = (await self.connection.execute(select(Region))).scalars().all()
        reg_ids = list(map(lambda x: x.id, db_regions))

        db_districts = (await self.connection.execute(select(District))).scalars().all()
        dis_ids = list(map(lambda x: x.id, db_districts))

        db_cities = (await self.connection.execute(select(City))).scalars().all()
        cit_ids = list(map(lambda x: x.id, db_cities))

        # данные, спаршенные из внешних сервисов, которых нет в бд
        appended_regions = list(filter(lambda x: x.id not in reg_ids, self.DataClass.regions))
        appended_districts = list(filter(lambda x: x.id not in dis_ids, self.DataClass.districts))
        appended_cities = list(filter(lambda x: x.id not in cit_ids, self.DataClass.cities))

        # ДОБАВЛЯЕМ НОВЫЕ ДАННЫЕ В БД
        self.connection.add_all(appended_regions)
        self.connection.add_all(appended_districts)
        self.connection.add_all(appended_cities)

        # обновляем дату последнего обращения
        appeal_date = (await self.connection.execute(select(LastAppealDate))).scalars().first()
        if appeal_date:
            appeal_date.date = datetime.now(tz=pytz.UTC)
        else:
            self.connection.add(LastAppealDate(date=datetime.now(tz=pytz.UTC)))
        await self.connection.commit()

        return 'данные успешно обновлены'






