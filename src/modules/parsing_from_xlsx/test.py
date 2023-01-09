from typing import Optional

import pandas as pd
from pydantic import BaseModel


class People(BaseModel):
    woman: Optional[int]
    man: Optional[int]


class City(BaseModel):
    name: str
    type: str
    region: Optional[str]
    people: Optional[People]


df = pd.read_excel(r'../../input_data/tab-5_VPN-2020.xlsx')
res = []
for idx, x in enumerate(df['Объект'].tolist()):
    if 'г. ' in x:
        pep = People(woman=df['Женщины'].tolist()[idx], man=df['Мужчины'].tolist()[idx])
        arr = df['Объект'].tolist()[:idx]
        i = len(arr)-1
        while i > 0 and not 'область' in arr[i]:
            i -= 1
        region = arr[i]
        res.append(City(name=x.partition('г. ')[2], type='город', people=pep, region=region))
    # if '- пгт ' in x:
    #     res.append(City(name=x.partition('- пгт ')[2], type='поселок городского типа'))
    # if 'п. ' in x:
    #     res.append(City(name=x.partition('п. ')[2], type='поселок'))
    # if 'село ' in x:
    #     res.append(City(name=x.partition('село ')[2], type='село'))

print(res)
