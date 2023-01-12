import uuid
from typing import Optional, List

import pandas as pd
from pydantic import BaseModel


class People:
    guid: uuid.UUID
    type: str
    all: Optional[int]
    woman: Optional[int]
    man: Optional[int]
    woman_perc: Optional[float]
    man_perc: Optional[float]

    def __init__(self, type, all, woman, man, woman_perc, man_perc):
        self.guid = uuid.uuid4()
        self.type = type
        self.all = all
        self.woman = woman
        self.man = man
        self.woman_perc = woman_perc
        self.man_perc = man_perc


class Population:
    guid: uuid.UUID
    urban_people: uuid.UUID
    rural_people: uuid.UUID

    def __init__(self, urban_people, rural_people):
        self.guid = uuid.uuid4()
        self.urban_people = urban_people
        self.rural_people = rural_people


class Country:
    guid: uuid.UUID
    name: str
    population: uuid.UUID

    def __init__(self, name, population):
        self.guid = uuid.uuid4()
        self.name = name
        self.population = population


class FederalDis:
    name: str
    guid: uuid.UUID
    country_guid: uuid.UUID
    population: uuid.UUID

    def __init__(self, name, population, country_guid):
        self.guid = uuid.uuid4()
        self.name = name
        self.population = population
        self.country_guid = country_guid


class Region:
    guid: uuid.UUID
    name: str
    district_guid: uuid.UUID
    population: uuid.UUID

    def __init__(self, name, population, district_guid):
        self.guid = uuid.uuid4()
        self.name = name
        self.population = population
        self.district_guid = district_guid


class AutDis:
    guid: uuid.UUID
    name: str
    region_guid: uuid.UUID
    population: uuid.UUID

    def __init__(self, name, population, region_guid):
        self.guid = uuid.uuid4()
        self.name = name
        self.population = population
        self.region_guid = region_guid


class City:
    guid: uuid.UUID
    region_guid: uuid.UUID
    name: str
    type: str
    people: uuid.UUID

    def __init__(self, name, people, region_guid, type):
        self.guid = uuid.uuid4()
        self.name = name
        self.people = people
        self.region_guid = region_guid
        self.type = type


def check_people_value(val):
    if val == '-':
        return None
    else:
        return val


class XlsxSettlementsParser:
    country: List[Country]
    federals: List[FederalDis]
    regions: List[Region]
    aut_dises: List[AutDis]
    local_objects: List[City]
    peoples: List[People]
    pops: List[Population]

    def __init__(self):
        self.dataframe = pd.read_excel(
            r'C:\Users\Stas\Desktop\GitHub\settlements-RF_backend\src\input_data\tab-5_VPN-2020.xlsx')
        self.peoples = []
        self.pops = []
        self.country = [self.create_country()]
        self.federals = self.create_federals(self.country)
        self.regions = self.create_regions(self.federals)
        self.aut_dises = self.create_auto_dists(self.regions)
        self.local_objects = self.parse_local_objects(self.regions)

    def define_pop(self, index):
        urban = People(type='городское',
                       all=check_people_value(self.dataframe['Мужчины и женщины'].tolist()[index + 1]),
                       woman=check_people_value(self.dataframe['Женщины'].tolist()[index + 1]),
                       man=check_people_value(self.dataframe['Мужчины'].tolist()[index + 1]),
                       woman_perc=check_people_value(self.dataframe['женщины в процентах'].tolist()[index + 1]),
                       man_perc=check_people_value(self.dataframe['мужчины в процентах'].tolist()[index + 1]))
        rural = People(type='сельское', all=check_people_value(self.dataframe['Мужчины и женщины'].tolist()[index + 2]),
                       woman=check_people_value(self.dataframe['Женщины'].tolist()[index + 2]),
                       man=check_people_value(self.dataframe['Мужчины'].tolist()[index + 2]),
                       woman_perc=check_people_value(self.dataframe['женщины в процентах'].tolist()[index + 2]),
                       man_perc=check_people_value(self.dataframe['мужчины в процентах'].tolist()[index + 2]))
        self.peoples.append(urban)
        self.peoples.append(rural)
        res = Population(urban_people=urban.guid, rural_people=rural.guid)
        self.pops.append(res)
        return res

    def create_country(self):
        return Country(name=self.dataframe['Объект'].tolist()[0], population=self.define_pop(0).guid)

    def create_federals(self, country):
        res = []
        for idx, x in enumerate(self.dataframe['Объект'].tolist()):
            if 'федеральный округ' in x:
                res.append(FederalDis(name=x, country_guid=country[0].guid, population=self.define_pop(idx).guid))
        return res

    def create_regions(self, federals):
        res = []
        for idx, x in enumerate(self.dataframe['Объект'].tolist()):
            if 'без' not in x:
                if 'область' in x or 'Республика' in x:
                    sliced_frame = self.dataframe['Объект'].tolist()[:idx]
                    i = len(sliced_frame) - 1
                    while i > 0 and 'федеральный округ' not in sliced_frame[i]:
                        i -= 1
                    fed = sliced_frame[i]
                    fed_guid = list(filter(lambda z: z.name == fed, federals))[0].guid
                    res.append(Region(name=x, district_guid=fed_guid, population=self.define_pop(idx).guid))
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
                res.append(AutDis(name=x, region_guid=reg_guid, population=self.define_pop(idx).guid))
        return res

    def create_local_object(self, obj, index, type, separator, regions):
        pop_type = 'городское'
        if type == 'поселок' or type == 'село':
            pop_type = 'сельское'
        population = People(type=pop_type, all=check_people_value(self.dataframe['Мужчины и женщины'].tolist()[index]),
                            woman=check_people_value(self.dataframe['Женщины'].tolist()[index]),
                            man=check_people_value(self.dataframe['Мужчины'].tolist()[index]),
                            woman_perc=check_people_value(self.dataframe['женщины в процентах'].tolist()[index]),
                            man_perc=check_people_value(self.dataframe['мужчины в процентах'].tolist()[index]))
        self.peoples.append(population)
        sliced_frame = self.dataframe['Объект'].tolist()[:index]
        i = len(sliced_frame) - 1
        while i > 0 and ('область' not in sliced_frame[i] or 'без ' in sliced_frame[i]) \
                    and ('Республика' not in sliced_frame[i] or 'без ' in sliced_frame[i]):
            i -= 1
        region = sliced_frame[i]
        print(region)
        reg_guid = list(filter(lambda z: z.name == region, regions))[0].guid
        name = obj
        if separator:
            name = obj.partition(separator)[2]
        return City(name=name, type=type, people=population.guid, region_guid=reg_guid)

    def parse_local_objects(self, regions):
        res = []
        for idx, x in enumerate(self.dataframe['Объект'].tolist()):
            if 'население' not in x:
                if 'г. ' in x:
                    res.append(self.create_local_object(x, idx, 'город', 'г. ', regions))
                if '- пгт ' in x:
                    res.append(self.create_local_object(x, idx, 'поселок городского типа', '- пгт ', regions))
                if 'п. ' in x:
                    res.append(self.create_local_object(x, idx, 'поселок', 'п. ', regions))
                if 'поселок' in x and 'п. ' not in x:
                    res.append(self.create_local_object(x, idx, 'поселок', 'поселок ', regions))
                if 'село ' in x:
                    res.append(self.create_local_object(x, idx, 'село', 'село ', regions))
                if 'Сельское поселение' in x and 'село ' not in x:
                    res.append(self.create_local_object(x, idx, 'село', None, regions))
        return res
