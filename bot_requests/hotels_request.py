from bot_requests.api_requests import api_request
import json
from telebot.types import InputMediaPhoto
import urllib
from urllib import request
import re
import os


def find_photos(hotel_id, photos):
    """Функция, создающая запрос к API и возвращает список фотографий определенного отеля"""
    payload_2 = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    response = api_request(method_endswith='properties/v2/get-summary', params=payload_2, method_type='POST')

    hotel_data = json.loads(response.text)

    photos_data = hotel_data['data']['propertyInfo']['propertyGallery']['images']

    photos_list = list()

    if len(photos_data) < photos:
        photos = len(photos_data)

    for j in range(photos):
        photo_url = photos_data[j]["image"]["url"][:-34]
        photo = InputMediaPhoto(photo_url)

        photos_list.append(photo)

    return photos_list


def get_data(hotel, days):
    """Функция, которая обрабатывает полученный от API ответ и возвращает словарь с информацией по отелю"""
    data = dict()
    data['id'] = hotel['id']
    data['name'] = hotel['name']
    data['lat'] = hotel['mapMarker']['latLong']['latitude']
    data['long'] = hotel['mapMarker']['latLong']['longitude']
    data['price'] = '$' + str(int(hotel['price']['lead']['amount']))
    data['dist'] = hotel['destinationInfo']['distanceFromDestination']['value']
    data['total_price'] = '$' + str(int(hotel['price']['lead']['amount']) * days)

    return data


def find_hotels(region, date_in, date_out, low_high, photos, i=0):
    """Функция, которая ищет отели по заданным пользователем параметрами"""

    days = int(re.search('\d*', str(date_out - date_in)).group(0))
    date_1_in = str(date_in).split('-')
    date_1_out = str(date_out).split('-')
    min, max = 10, 300

    if low_high == '/lowprice':
        min = 10
        max = 300
    elif low_high == '/highprice':
        min = 100
        max = 1500

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": f"{region}"},
        "checkInDate": {
            "day": int(date_1_in[2]),
            "month": int(date_1_in[1]),
            "year": int(date_1_in[0])
        },
        "checkOutDate": {
            "day": int(date_1_out[2]),
            "month": int(date_1_out[1]),
            "year": int(date_1_out[0])
        },
        "rooms": [
            {
                "adults": 2
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": max,
            "min": min
        }}
    }

    response = api_request(method_endswith='properties/v2/list', params=payload, method_type='POST')
    hotels_data = json.loads(response.text)

    hotels = hotels_data['data']['propertySearch']['properties']

    data = dict()
    data_2 = list()

    if low_high == '/lowprice':
        data = get_data(hotels[i], days)
        data_2 = list()
        if photos != 0:
            data_2 = find_photos(hotels[i]['id'], photos)

    elif low_high == '/highprice':
        data = get_data(hotels[- i - 1], days)
        data_2 = list()
        if photos != 0:
            data_2 = find_photos(hotels[- i - 1]['id'], photos)

    return data, data_2


def find_best_hotel(hotels_amount, region, date_in, date_out, photos, min_price, max_price, dist):
    """Функция, которая ищет отели по заданным пользователем параметрами команды bestdeal"""

    days = int(re.search('\d*', str(date_out - date_in)).group(0))
    date_1_in = str(date_in).split('-')
    date_1_out = str(date_out).split('-')

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": f"{region}"},
        "checkInDate": {
            "day": int(date_1_in[2]),
            "month": int(date_1_in[1]),
            "year": int(date_1_in[0])
        },
        "checkOutDate": {
            "day": int(date_1_out[2]),
            "month": int(date_1_out[1]),
            "year": int(date_1_out[0])
        },
        "rooms": [
            {
                "adults": 2
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": max_price,
            "min": min_price
        }}
    }

    response = api_request(method_endswith='properties/v2/list', params=payload, method_type='POST')
    hotels_response = json.loads(response.text)

    hotels = hotels_response['data']['propertySearch']['properties']
    hotels_data = list()

    accept_hotels = list()
    n = 0
    for hotel in hotels:
        if hotel['destinationInfo']['distanceFromDestination']['value'] < dist:
            accept_hotels.append(n)
        n += 1
        if hotels_amount == len(accept_hotels):
            break

    for i in accept_hotels:
        data = get_data(hotels[i], days)
        photo_data = list()
        if photos != 0:
            photo_data = find_photos(hotels[i]['id'], photos)
        hotels_data.append((data, photo_data))

    if len(hotels_data) == 0:
        raise TypeError

    return hotels_data
