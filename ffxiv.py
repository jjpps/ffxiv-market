from dotenv import load_dotenv
import os
import asyncio
import logging
import json
import aiohttp
import pyxivapi
from Item import Item

from pyxivapi.models import Filter, Sort
client = pyxivapi.XIVAPIClient(api_key=os.environ['xivapi_key'])
async def getItemByName(name):    
    # Item search with paging
    item = await client.index_search(
        name=name,
        indexes=["Recipe","Item"],
        columns=["ID","Name","Icon","UrlType"],
        page=0,
        per_page=10
    )
    await client.session.close()
    print(item['Results'])
    return item['Results'][0]

async def getItemById(id):
    
    item = await client.index_by_id(
        index=id,
        columns=["ID","Name","Icon","UrlType"]
    )
    await client.session.close()
    return item['Results'][0]




if __name__ == '__main__':   
    load_dotenv()  # This line brings all environment variables from .env into os.environ
    #print("Chave xivapi_key", os.environ['xivapi_key']) 
    #logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    loop = asyncio.get_event_loop()
    item = Item(loop.run_until_complete(getItemByName("Indagator's Helmet of Gathering")))
    print(f"Encontrado item {item.ID} - {item.Name}")

   
    