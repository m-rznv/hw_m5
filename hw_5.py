import asyncio
import aiohttp
import datetime

currency_list = [
'AUD',
'CAD',
'CZK',
'DKK',
'HUF',
'ILS',
'JPY',
'LVL',
'LTL',
'NOK',
'SKK',
'SEK',
'CHF',
'GBP',
'USD',
'BYR',
'EUR',
'GEL',
'PLZ'
]



async def request(url):
    try:
        connector = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    data = await response.json()
                    return data
      
    except aiohttp.ClientConnectionError as e:
        print(f'Error: {e}')
        return None
    
 
async def main(days, currency):
    urls = []
    for i in range(days):
        date_request = datetime.datetime.now() - datetime.timedelta(days=i)
        print(date_request)
        date_request = date_request.strftime('%d.%m.%Y')
        print(date_request)
        url = f'https://api.privatbank.ua/p24api/exchange_rates?date={date_request}'
        if request(url):
            urls.append(request(url))
        
    result = await asyncio.gather(*urls)
    for data in result:
        result = '--------------\n'
        result += f'Date: {data["date"]}\n'
        for cur in currency:
            cur = cur.upper()
            for i in data['exchangeRate']:
                if i['currency'] == cur:
                    result += f'{cur}: sale: {i["saleRate"]} buy: {i["purchaseRate"]}\n'
                    result += '--------------\n'
        
        print(result)


if __name__ == '__main__':
    res = []
    res.append(input('Choose at least one currency and press enter '))
    while True:
        ot_req = input('Add another currency? ')
        if ot_req:
            res.append(ot_req)
        else:
            break
    day = input('For what period to display the result? (maximum 10 days) ')
    asyncio.run(main(int(day), res))
    



