import requests
from bot_requests.api_requests import api_request
import json
import re


def api_reques(method_endswith, params, method_type):
    """Функция, создающая запросы к API"""
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    headers = {
        'content-type': 'application/json',
        #'X-RapidAPI-Key': "49a222e3f9msh707cc06b668f5d0p1f8ee9jsn149c62888e4b",
        'X-RapidAPI-Key': "d17b6fd198mshd3cfdcc33b8b250p15a640jsnf8b34aefa962",
        # 'X-RapidAPI-Host': "hotels4.p.rapidapi.com"
        'X-RapidAPI-Host': "hotels4.p.rapidapi.com"
    }

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params,
            headers=headers
        )
    else:
        return post_request(
            url=url,
            params=params,
            headers=headers
        )


def get_request(url, params, headers):
    """Функция, создающая GET запросы к API"""
    response = requests.get(
        url=url,
        headers=headers,
        params=params,
        timeout=30
    )
    if response.status_code == requests.codes.ok:
        return response


def post_request(url, params, headers):
    """Функция, создающая POST запросы к API"""
    response_1 = requests.request(
        method='POST',
        url=url,
        headers=headers,
        json=params,
        timeout=30
    )
    if response_1.status_code == requests.codes.ok:
        return response_1


def find_hotels():
    """Функция, которая ищет отели по заданным пользователем параметрами"""

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {
            "regionId": "6054439"
        },
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [
                    {
                        "age": 5
                    },
                    {
                        "age": 7
                    }
                ]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {
            "price": {
                "max": 150,
                "min": 100
            }
        }
    }

    # payload = {
    #     "currency": "USD",
    #     "eapid": 1,
    #     "locale": "ru_RU",
    #     "siteId": 300000001,
    #     "destination": {"regionId": 6278809},
    #     "checkInDate": {
    #         "day": 2,
    #         "month": 8,
    #         "year": 2024
    #     },
    #     "checkOutDate": {
    #         "day": 8,
    #         "month": 8,
    #         "year": 2024
    #     },
    #     "rooms": [
    #         {
    #             "adults": 2
    #         }
    #     ],
    #     "resultsStartingIndex": 0,
    #     "resultsSize": 200,
    #     "sort": "PRICE_LOW_TO_HIGH",
    #     "filters": {"price": {
    #         "max": 500,
    #         "min": 50
    #     }}
    # }

    response = api_request(method_endswith='properties/v2/list', params=payload, method_type='POST')
    hotels_data = json.loads(response.text)



    print(hotels_data)

find_hotels()