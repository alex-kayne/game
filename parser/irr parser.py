import asyncio
import aiohttp
from urls import urls
from bs4 import BeautifulSoup
import requests
async def fetch_content(url):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            data = await response.read()
            return write_to_dict(data, url)

def write_to_dict(data, url):
    soup = BeautifulSoup(data, 'lxml')
    soup.decode('utf-8')
    header = soup.find_all('h1', class_='productPage__title js-productPageTitle')
    all_items = soup.find_all('li', class_='productPage__infoColumnBlockText')
    all_items = list(map(lambda x: x.text, all_items))
    values_dict = {}
    header = ''.join(map(lambda x: x.text, header)).strip()
    values_dict['header'] = header
    values_dict['url'] = url
    for item in all_items:
        if item.find('Этаж:') == 0:
            values_dict['floor'] = item.strip('Этаж:').strip()
        elif item.find('Комнат в квартире:') == 0:
            values_dict['rooms'] = item.strip('Комнат в квартире:').strip()
        elif item.find('Этажей в здании:') == 0:
            values_dict['floors'] = item.strip('Этажей в здании:').strip()
        elif item.find('Общая площадь:') == 0:
            values_dict['general_square'] = ''.join(list(map(lambda x: x if x.isdigit() or x == '.' else '', item.strip('м2'))))
        elif item.find('Жилая площадь:') == 0:
            values_dict['living_space'] = ''.join(list(map(lambda x: x if x.isdigit() or x == '.' else '', item.strip('м2'))))
        elif item.find('Площадь кухни:') == 0:
            values_dict['kitchen_area'] = ''.join(list(map(lambda x: x if x.isdigit() or x == '.' else '', item.strip('м2'))))
        elif item.find('Улица:') == 0:
            values_dict['street'] = item.strip('Улица:').strip()
        elif item.find('Дом:') == 0:
            values_dict['house'] = item.strip('Дом:').strip()
        elif item.find('Метро:') == 0:
            values_dict['metro_station'] = item.strip('Метро:').strip()
        else:
            if 'additional' not in values_dict:
                values_dict['additional'] = [item]
            else:
                values_dict['additional'].append(item)
    return values_dict



def write_to_file():
    with open(f'parsed_data.txt', 'w', encoding='utf-8') as file:
        for i in output_list:
            file.write(f'{i}\n')

async def main(urls):
    tasks = [fetch_content(url) for url in urls]
        #for url in urls:
            #task = asyncio.create_task(fetch_content(url, session))
        #    task =
        #    tasks.append(task)

    response = await asyncio.gather(*tasks, return_exceptions=True)
    print(response)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
    loop.run_until_complete(asyncio.sleep(1))
    loop.close()

    # перенести gather