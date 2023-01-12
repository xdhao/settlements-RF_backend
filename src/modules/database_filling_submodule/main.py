from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.database_filling_submodule.routes.db_filling_router import FillingDatabaseModule

app = FastAPI(docs_url="/api/filling-db-module/docs", redoc_url="/api/filling-db-module/redoc", openapi_url='/api/filling-db-module/openapi.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(FillingDatabaseModule.routes(), prefix="/api")
