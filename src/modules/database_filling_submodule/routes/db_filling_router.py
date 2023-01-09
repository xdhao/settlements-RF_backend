from class_based_fastapi import Routable, get
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.core_websoursces.database.database import get_session
from modules.database_filling_submodule.reps.FillingDatabaseRepository import FillingDatabaseRepository


class FillingDatabaseModule(Routable):
    BASE_TEMPLATE_PATH = '/{module}/v{version}/{user_path}'
    NAME_MODULE = 'filling_db_module'
    db: AsyncSession = Depends(get_session)

    def __init__(self):
        self.repository = FillingDatabaseRepository(connection=self.db)

    @get("fill-with-data-from-fias-api-and-wikidata", response_model=str)
    async def filling_with_fias_wikidata(self):
        return await self.repository.fill_database()

    @get("fill-with-json", response_model=str)
    async def filling_with_json(self):
        return await self.repository.fill_database()
