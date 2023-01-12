import uuid
from typing import Optional

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column, Relationship

from core.core_xlsx_parser.models.People import People
from core.core_xlsx_parser.models.SomeRegion import SomeRegion


class LocalSubject(Base, table=True):
    name: str
    type: str
    region_guid: uuid.UUID = Field(foreign_key=SomeRegion.__pk__, nullable=True)
    people: uuid.UUID = Field(foreign_key=People.__pk__, nullable=True)

    people_obj: Optional[People] = Relationship()
    region_obj: Optional[SomeRegion] = Relationship()

