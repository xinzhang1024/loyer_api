
import requests
from utils.helpers import load_csv_file, load_json_file


def get_apartment_rent():
    return load_csv_file("resources", "indicateurs-loyers-appartements")


def get_maison_rent():
    return load_csv_file("resources", "indicateurs-loyers-maisons")


def get_city_list(dep):
    res = requests.get(f'https://geo.api.gouv.fr/departements/{dep}/communes?fields=nom,code,codesPostaux,population&format=json&geometry=centre')

    if res.status_code != 200:
        return {}

    if dep == '75':
        new_res = []
        paris = res.json()[0]
        codes_postaux = paris.get('codesPostaux')

        for item in codes_postaux:
            code = item[:2] + '1' + item[3:]
            new_res.append({
                'nom': paris.get('nom'),
                'code': code,
                'codesPostaux': [item],
                'population': paris.get('population')
            })
        return new_res

    return res.json()


def get_city_score(name):
    # city_score.json is generated by scrapy from website, scrapy code path: utils/scrapy.py
    city_score = load_json_file("resources", "city_score")
    if name.startswith('Paris'):
        name = 'Paris'

    for item in city_score:
        if name.strip().lower() == item.get('city').strip().lower():
            return float(item.get('score'))

    return 0.0
