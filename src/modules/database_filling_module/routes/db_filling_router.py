from class_based_fastapi import Routable, get, put, post, delete
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database.database import get_session
from modules.database_filling_module.reps.FillingDatabaseRepository import FillingDatabaseRepository


class FillingDatabaseModule(Routable):
    BASE_TEMPLATE_PATH = '/{module}/v{version}/{user_path}'
    NAME_MODULE = 'filling_db_module'
    db: AsyncSession = Depends(get_session)

    def __init__(self):
        self.repository = FillingDatabaseRepository(connection=self.db)

    @get("fill-the-database", response_model=str)
    async def get_users(self):
        return await self.repository.fill_database()
