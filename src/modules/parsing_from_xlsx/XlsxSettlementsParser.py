import uuid
from typing import Optional, List

import pandas as pd
from pydantic import BaseModel


class People(BaseModel):
    all: Optional[int]
    woman: Optional[int]
    man: Optional[int]
    woman_perc: Optional[float]
    man_perc: Optional[float]


class Population(BaseModel):
    urban: Optional[People]
    rural: Optional[People]


class Country(BaseModel):
    guid: uuid.UUID = uuid.uuid4()
    name: str
    population: Optional[Population]


class FederalDis(BaseModel):
    name: str
    guid: uuid.UUID = uuid.uuid4()
    country_guid: uuid.UUID
    population: Optional[Population]


class Region(BaseModel):
    guid: uuid.UUID = uuid.uuid4()
    name: str
    district_guid: uuid.UUID
    population: Optional[Population]


class AutDis(BaseModel):
    name: str
    region_guid: uuid.UUID
    population: Optional[Population]


class City(BaseModel):
    region_guid: uuid.UUID
    name: str
    type: str
    people: Optional[People]


def check_people_value(val):
    if val == '-':
        return None
    else:
        return val


class XlsxSettlementsParser:
    country: Country
    federals: List[FederalDis]
    regions: List[Region]
    aut_dises: List[AutDis]
    local_objects: List[City]

    def __init__(self):
        self.dataframe = pd.read_excel(r'../../input_data/tab-5_VPN-2020.xlsx')
        self.country = self.create_country()
        self.federals = self.create_federals(self.country)
        self.regions = self.create_regions(self.federals)
        self.aut_dises = self.create_auto_dists(self.regions)
        self.local_objects = self.parse_local_objects(self.regions)

    def define_pop(self, index):
        urban = People(all=check_people_value(self.dataframe['Мужчины и женщины'].tolist()[index + 1]),
                       woman=check_people_value(self.dataframe['Женщины'].tolist()[index + 1]),
                       man=check_people_value(self.dataframe['Мужчины'].tolist()[index + 1]),
                       woman_perc=check_people_value(self.dataframe['женщины в процентах'].tolist()[index + 1]),
                       man_perc=check_people_value(self.dataframe['мужчины в процентах'].tolist()[index + 1]))
        rural = People(all=check_people_value(self.dataframe['Мужчины и женщины'].tolist()[index + 2]),
                       woman=check_people_value(self.dataframe['Женщины'].tolist()[index + 2]),
                       man=check_people_value(self.dataframe['Мужчины'].tolist()[index + 2]),
                       woman_perc=check_people_value(self.dataframe['женщины в процентах'].tolist()[index + 2]),
                       man_perc=check_people_value(self.dataframe['мужчины в процентах'].tolist()[index + 2]))
        return Population(urban=urban, rural=rural)

    def create_country(self):
        return Country(name=self.dataframe['Объект'].tolist()[0])

    def create_federals(self, country):
        res = []
        for idx, x in enumerate(self.dataframe['Объект'].tolist()):
            if 'федеральный округ' in x:
                res.append(FederalDis(name=x, country_guid=country.guid, population=self.define_pop(idx)))
        return res

    def create_regions(self, federals):
        res = []
        for idx, x in enumerate(self.dataframe['Объект'].tolist()):
            if 'область' in x:
                sliced_frame = self.dataframe['Объект'].tolist()[:idx]
                i = len(sliced_frame) - 1
                while i > 0 and 'федеральный округ' not in sliced_frame[i]:
                    i -= 1
                fed = sliced_frame[i]
                fed_guid = list(filter(lambda z: z.name == fed, federals))[0].guid
                res.append(Region(name=x, district_guid=fed_guid, population=self.define_pop(idx)))
        return res

    def create_auto_dists(self, regions):
        res = []
        for idx, x in enumerate(self.dataframe['Объект'].tolist()):
            if 'автономный округ' in x:
                sliced_frame = self.dataframe['Объект'].tolist()[:idx]
                i = len(sliced_frame) - 1
                while i > 0 and 'область' not in sliced_frame[i]:
                    i -= 1
                reg = sliced_frame[i]
                reg_guid = list(filter(lambda z: z.name == reg, regions))[0].guid
                res.append(AutDis(name=x, region_guid=reg_guid, population=self.define_pop(idx)))
        return res

    def create_local_object(self, obj, index, type, separator, regions):
        population = People(all=check_people_value(self.dataframe['Мужчины и женщины'].tolist()[index]),
                            woman=check_people_value(self.dataframe['Женщины'].tolist()[index]),
                            man=check_people_value(self.dataframe['Мужчины'].tolist()[index]),
                            woman_perc=check_people_value(self.dataframe['женщины в процентах'].tolist()[index]),
                            man_perc=check_people_value(self.dataframe['мужчины в процентах'].tolist()[index]))
        sliced_frame = self.dataframe['Объект'].tolist()[:index]
        i = len(sliced_frame) - 1
        while i > 0 and 'область' not in sliced_frame[i]:
            i -= 1
        region = sliced_frame[i]
        reg_guid = list(filter(lambda z: z.name == region, regions))[0].guid
        return City(name=obj.partition(separator)[2], type=type, people=population, region_guid=reg_guid)

    def parse_local_objects(self, regions):
        res = []
        for idx, x in enumerate(self.dataframe['Объект'].tolist()):
            if 'г. ' in x:
                res.append(self.create_local_object(x, idx, 'город', 'г. ', regions))
            if '- пгт ' in x:
                res.append(self.create_local_object(x, idx, 'поселок городского типа', '- пгт ', regions))
            if 'п. ' in x:
                res.append(self.create_local_object(x, idx, 'поселок', 'п. ', regions))
            if 'село ' in x:
                res.append(self.create_local_object(x, idx, 'село', 'село ', regions))
        return res


