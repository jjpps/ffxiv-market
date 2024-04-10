from dotenv import load_dotenv
import os
import asyncio
import logging
import json
import aiohttp
import pyxivapi
from Item import Item

from pyxivapi.models import Filter, Sort


async def getItemByName(name):
    client = pyxivapi.XIVAPIClient(api_key=os.environ['xivapi_key'])

    # Item search with paging
    itemResultado = await client.index_search(
        name=name,
        indexes=["Recipe"],
        columns=["ID","Name","Icon","UrlType"],
        page=0,
        per_page=10
    )
    await client.session.close()
    return itemResultado['Results'][0]


if __name__ == '__main__':   
    load_dotenv()  # This line brings all environment variables from .env into os.environ
    #print("Chave xivapi_key", os.environ['xivapi_key']) 
    #logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    loop = asyncio.get_event_loop()
    item = Item(loop.run_until_complete(getItemByName("Indagator's Helmet of Gathering")))
    
   
    