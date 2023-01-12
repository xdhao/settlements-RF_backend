from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.excel_data_module.routes import excel_data_router
from modules.excel_data_module.routes.excel_data_router import ExcelDataRouter

app = FastAPI(docs_url="/api/excel-data/docs", redoc_url="/api/excel-data/redoc", openapi_url='/api/excel-data/openapi.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(ExcelDataRouter.routes(), prefix="/api")
app.include_router(excel_data_router.router, prefix="/api")

