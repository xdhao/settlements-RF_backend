import uuid

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column

from core.core_xlsx_parser.models.Population import Population
from core.core_xlsx_parser.models.Region import Region


class AutonomicDistrict(Base, table=True):
    name: str
    region_guid: uuid.UUID = Field(foreign_key=Region.__pk__, nullable=True)
    population: uuid.UUID = Field(foreign_key=Population.__pk__, nullable=True)


