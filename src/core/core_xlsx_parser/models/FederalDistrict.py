import uuid

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column

from core.core_xlsx_parser.models.Country import Country
from core.core_xlsx_parser.models.Population import Population


class FederalDistrict(Base, table=True):
    country_guid: uuid.UUID = Field(foreign_key=Country.__pk__, nullable=True)
    population: uuid.UUID = Field(foreign_key=Population.__pk__, nullable=True)


