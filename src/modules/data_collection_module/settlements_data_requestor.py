from typing import List

import requests
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

from modules.data_collection_module.schemas.BasicSettlementsObjects import Region, City, District


def get_ru_alphabet():
    a = ord('а')
    return [chr(i) for i in range(a, a + 6)] + [chr(a + 33)] + [chr(i) for i in range(a + 6, a + 32)]


class SettlementsDataRequestor:
    regions: List[Region]
    districts = List[District]
    cities = List[City]

    def __init__(self):
        self.wikidata_url = "https://query.wikidata.org/sparql"  # ссылка на wikidata

        self.regions = self.get_regions()
        self.districts = self.get_districts(self.regions)
        self.cities = self.get_cities(self.regions, self.districts)

    def get_wikidata(self, endpoint_url, object):
        query = """SELECT ?place ?place_coord ?place_pop ?place_area ?name ?head ?headLabel ?parent ?parentLabel WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          ?place wdt:P17 wd:Q159;
            wdt:P31 wd:Q486972.
          OPTIONAL {
            ?place rdfs:label ?name.
            FILTER((LANG(?name)) = "ru")
          }
          FILTER(STRSTARTS(?name, "%s"))
          OPTIONAL { ?place wdt:P625 ?place_coord. }
          OPTIONAL { ?place wdt:P1082 ?place_pop. }
          OPTIONAL { ?place wdt:P2046 ?place_area. }
          OPTIONAL { ?place wdt:P6 ?head. }
          OPTIONAL { ?place wdt:P131 ?parent. }
        }""" % object

        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def get_regions(self):
        """
        Kladr api возвращает ответ только при заданном параметре query
        для получения всех регионов РФ отправим запрос для каждой буквы алфавита
        """
        arr = get_ru_alphabet()
        res = list()
        # for a in arr:
        url = 'https://kladr-api.ru/api.php?query=Арх&contentType=region&limit=1'
        data = requests.get(url)
        data = data.json()
        for x in data['result']:
            if x['name'] != 'Бесплатная версия kladr-api.ru':
                name = x['name']
                if x['type'] == 'Область':
                    name = x['name'] + ' область'
                y = Region(name=name, id=x['id'], type=x['type'])
                res.append(y)
        return res

    def get_districts(self, parents):
        """
        :param parents: список регионов
        :return: список районов
        """
        res = list()
        for parent in parents:
            url = f'https://kladr-api.ru/api.php?contentType=district&regionId={parent.id}&limit=1'
            data = requests.get(url)
            data = data.json()
            for x in data['result']:
                if x['name'] != 'Бесплатная версия kladr-api.ru':
                    y = District(id=x['id'], region_id=parent.id, name=x['name'], type=x['type'])
                    res.append(y)
        return res

    def get_cities(self, regions, districts):

        res = list()
        for region in regions:
            url = f'https://kladr-api.ru/api.php?contentType=city&regionId={region.id}&limit=1'
            data = requests.get(url)
            data = data.json()
            for x in data['result']:
                if x['name'] != 'Бесплатная версия kladr-api.ru':
                    wikidata = self.get_wikidata(self.wikidata_url, x['name'])
                    head, area, people = (None for _ in range(3))
                    if len(wikidata) < 2:
                        for result in wikidata["results"]["bindings"]:
                            if 'headLabel' in result and 'value' in result['headLabel']:
                                head = result['headLabel']['value']
                            if 'place_area' in result and 'value' in result['place_area']:
                                area = float(result['place_area']['value'])
                            if 'place_pop' in result and 'value' in result['place_pop']:
                                people = result['place_pop']['value']
                    y = City(id=x['id'], region_id=region.id, name=x['name'], type=x['type'],
                             head=head, area=area, people=people)
                    res.append(y)
        for district in districts:
            url = f'https://kladr-api.ru/api.php?contentType=city&districtId={district.id}&limit=1'
            data = requests.get(url)
            data = data.json()
            for x in data['result']:
                if x['name'] != 'Бесплатная версия kladr-api.ru':
                    for city in res:
                        if city.id == x['id']:
                            city.district_id = district.id
        return res


