import csv
from datetime import datetime
import requests
import json
import time
import aiofiles
import asyncio
from fake_useragent import UserAgent
from aiocsv import AsyncWriter

start_time = time.time()
ua = UserAgent()

headers = {
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://moonarch.app/',
    'Version': '2.14.0',
    'Origin': 'https://moonarch.app',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'If-None-Match': 'W/33a38-LCQHlBaA0m2t+6l0RhYnjhS/W3s',
}

params = {
    'full': '1',
}


async def collect_data():

    response = requests.get('https://api.moonarch.app/1.0/miners/list', params=params, headers=headers)

    result = []

    data = response.json()
    miners = data.get('miners')
    # print(f'Now {len(miners)} miners')

    async def hours_minutes(td):
        return f'{td.seconds // 3600} hour {(td.seconds // 60) % 60} minutes has passed'

    async def create_datetime(created_date):
        if (datetime.now() - created_date).days <= 0:
            if ((datetime.now() - created_date).seconds // 3600) <= 0:
                return f'{((datetime.now() - created_date).seconds // 60) % 60} minutes has passed'
            else:
                return f'{await hours_minutes(datetime.now() - created_date)}'
        else:
            return f'{(datetime.now() - created_date).days} days has passed'

    async with aiofiles.open('result.csv', 'w') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            (
                'Miner name',
                'Price',
                'Network',
                'Balance',
                'Balance for 7 days',
                'Balance for 24 days',
                'Fees',
                'SellFees',
                'Rate',
                'Url miner',
                'Contract',
                'Address',
                'Name coin',
                'Symbol',
                'Link Telegram',
                'Created date'
            )
        )

    for miner in miners:
        miner_name = miner.get('name')
        link_telegram = miner.get('telegram')
        network = miner.get('network')
        fees = miner.get('fees')
        sellFees = miner.get('sellFees')
        rate = miner.get('rate')
        url_miner = miner.get('url')
        contract = miner.get('contract')
        address = miner.get('token').get('address')
        price = miner.get('token').get('price')
        name_coin = miner.get('token').get('name')
        symbol = miner.get('token').get('symbol')
        balance = miner.get('balance')
        balance7d = miner.get('balance7d')
        balance24 = miner.get('balance24')
        date = await create_datetime(datetime.fromtimestamp(miner.get('created')))

        result.append(
            {
                'miner_name': miner_name,
                'price': price,
                'network': network,
                'balance': balance,
                'balance7d': balance7d,
                'balance24': balance24,
                'fees': fees,
                'sellFees': sellFees,
                'rate': rate,
                'url_miner': url_miner,
                'contract': contract,
                'address': address,
                'name_coin': name_coin,
                'symbol': symbol,
                'link_telegram': link_telegram,
                'created_date': date
            }
        )

        async with aiofiles.open('result.csv', 'a') as file:
            writer = AsyncWriter(file)

            await writer.writerow(
                (
                    miner_name,
                    price,
                    network,
                    balance,
                    balance7d,
                    balance24,
                    fees,
                    sellFees,
                    rate,
                    url_miner,
                    contract,
                    address,
                    name_coin,
                    symbol,
                    link_telegram,
                    date
                )
            )
    with open('result.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


async def main():
    await collect_data()


if __name__ == '__main__':
    asyncio.run(main())

print("--- %s seconds ---" % (time.time() - start_time))
