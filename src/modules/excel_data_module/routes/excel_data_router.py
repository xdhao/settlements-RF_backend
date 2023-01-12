import uuid
from typing import List

from class_based_fastapi import Routable, get
from fastapi import Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from core.core_xlsx_parser.database.database import get_session
from modules.excel_data_module.reps.ExcelDataRep import ExcelDataRepository
from modules.excel_data_module.schemas.view_models import CountryView, federal_DistrictView, SomeRegionView, AutDisView, \
    LocalObjectsSummary
from starlette.responses import FileResponse


class ExcelDataRouter(Routable):
    BASE_TEMPLATE_PATH = '/{module}/v{version}/{user_path}'
    NAME_MODULE = 'excel_data'
    db: AsyncSession = Depends(get_session)

    def __init__(self):
        self.repository = ExcelDataRepository(connection=self.db)

    @get("get-counties", response_model=List[CountryView])
    async def get_countries(self):
        return await self.repository.get_countries()

    @get("get-federal-districts", response_model=List[federal_DistrictView])
    async def get_federal_districts(self):
        return await self.repository.get_federals()

    @get("get-regions/{id}", response_model=List[SomeRegionView])
    async def get_some_regions(self, id: uuid.UUID):
        return await self.repository.get_regions(id)

    @get("get-autonomic-districts", response_model=List[AutDisView])
    async def get_autonomic_districts(self):
        return await self.repository.get_auto_districts()

    @get("get-local-objects/{id}", response_model=LocalObjectsSummary)
    async def get_local_objects(self, id: uuid.UUID):
        return await self.repository.get_local_objects(id)


router = APIRouter()


@router.get("/get-source-file", response_class=FileResponse)
async def get_source_file():
    path = "input_data/tab-5_VPN-2020.xlsx"
    file_name = "tab-5_VPN-2020.xlsx"
    return FileResponse(
        path, headers={'Content-Disposition': f'attachment;filename={file_name}'}
    )
