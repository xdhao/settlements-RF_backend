from class_based_fastapi import Routable, get
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.core_websoursces.database.database import get_session as get_session_1
from core.core_xlsx_parser.database.database import get_session as get_session_2

from modules.database_filling_submodule.reps.FillingDatabaseRepository import FillingDatabaseRepository


class FillingDatabaseModule(Routable):
    BASE_TEMPLATE_PATH = '/{module}/v{version}/{user_path}'
    NAME_MODULE = 'filling_db_module'
    db_webservices: AsyncSession = Depends(get_session_1)
    db_excel_parser: AsyncSession = Depends(get_session_2)

    def __init__(self):
        self.repository = FillingDatabaseRepository(connection_1=self.db_webservices, connection_2=self.db_excel_parser)

    @get("fill-with-data-from-fias-api-and-wikidata", response_model=str)
    async def filling_with_fias_wikidata(self):
        return await self.repository.fill_with_data_from_webservices()

    @get("fill-with-excel", response_model=str)
    async def filling_with_excel(self):
        return await self.repository.fill_with_data_from_excel()
