import uuid

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column

from core.core_xlsx_parser.models.People import People


class Population(Base, table=True):
    urban_people: uuid.UUID = Field(foreign_key=People.__pk__, nullable=True)
    rural_people: uuid.UUID = Field(foreign_key=People.__pk__, nullable=True)


