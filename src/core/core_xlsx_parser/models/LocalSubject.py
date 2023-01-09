import uuid

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column

from core.core_xlsx_parser.models.People import People
from core.core_xlsx_parser.models.SomeRegion import SomeRegion


class LocalSubject(Base, table=True):
    name: str
    type: str
    region_guid: uuid.UUID = Field(foreign_key=SomeRegion.__pk__, nullable=True)
    people: uuid.UUID = Field(foreign_key=People.__pk__, nullable=True)


