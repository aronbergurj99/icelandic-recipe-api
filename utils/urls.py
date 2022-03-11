from typing import List
import json
import requests

def gottimatinn_urls(
    number_of_urls: int,
    orderBy: str = 'created',
    orderDirection: str = 'DESC',
) -> List[str]:
    """ Returns recipe urls from gottimatinn.is, in specified order"""
    URL = f'https://www.gottimatinn.is/json/recipes/?orderby={orderBy}&orderDirection={orderDirection}&groupIds=&occasionIds=&countryIds=&authorIds=&difficulty=&page=1&pageSize={number_of_urls}&keywords='
    returnUrl = 'https://www.gottimatinn.is/uppskriftir/'
    res = json.loads(requests.get(URL).text)
    items = res['Items']
    return [returnUrl + data['Url'] for data in items]
