from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.fias_api_and_wikidata_module.routes.WebServicesDataRouter import WebServicesDataRouter, \
    WebServicesDataRouterV2

app = FastAPI(docs_url="/api/webservices_data/docs", redoc_url="/api/webservices_data/redoc", openapi_url='/api/webservices_data/openapi.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(WebServicesDataRouter.routes(), prefix="/api")
app.include_router(WebServicesDataRouterV2.routes(), prefix="/api")

