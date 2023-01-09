import uuid

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column

from core.core_xlsx_parser.models.Country import Country
from core.core_xlsx_parser.models.People import People


class LocalSubject(Base, table=True):
    region_guid: uuid.UUID = Field(foreign_key=Country.__pk__, nullable=True)
    urban_people: uuid.UUID = Field(foreign_key=People.__pk__, nullable=True)
    rural_people: uuid.UUID = Field(foreign_key=People.__pk__, nullable=True)


