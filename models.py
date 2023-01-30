# coding=utf-8
import asyncio
import random
import string
import typing

from aiogram import Bot, types
from asyncio import sleep

from aiogram.utils.exceptions import RetryAfter

from config import *
from aiohttp import ClientSession


async def add_item(client: ClientSession,
                   dc_id: int, hex_key: typing.Any,
                   premium: bool):
    ok = False

    z = ''.join([random.choice(string.digits) for _ in range(5)])

    def url(arg):
        return 'https://api.lolz.guru/market/{}'.format(arg)
    headers = {'Authorization': f'Bearer {LOLZ_KEY}'}

    while not ok:
        await asyncio.sleep(3)
        post_data = {
            'title': LOLZ_ACCOUNT_TITLE,
            'price': LOLZ_ACCOUNT_PRICE if not premium else LOLZ_ACCOUNT_PREMIUM_PRICE,
            'category_id': 24,
            'currency': 'rub',
            'item_origin': LOLZ_ACCOUNT_ORIGIN,
            'extended_guarantee': 0,
            'description': LOLZ_ACCOUNT_DESCRIPTION
        }

        sell = await client.post(url('item/add/'), data=post_data, headers=headers)
        if sell.status == 429:
            await asyncio.sleep(6)
            sell = await client.post(url('item/add/'), data=post_data, headers=headers)
        sell_json = await sell.json()
        item_id = sell_json['item']['item_id']
        try:
            print(f'[LOLZ {item_id}]', 'Аккаунт добавлен, и ожидает проверки')
        except:
            pass


        sell_data = {
            'login_password': str(hex_key)+':'+str(dc_id),
            'extra[checkChannels]': 1,
            'extra[checkSpam]': 1
        }

        await asyncio.sleep(3)
        checkout = await client.post(url(f'{item_id}/goods/check'), data=sell_data, headers=headers)
        if not checkout.ok:
            pass
        else:
            try:
                print(f'[LOLZ {item_id}] Аккаунт успешно загружен -> https://lolz.guru/market/{item_id}')
            except:
                pass
            return checkout


