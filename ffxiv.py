import os
import asyncio
import logging
import json
import aiohttp
import pyxivapi
#from dotenv import load_dotenv
from Item import Item
from RecipeClass import RecipeClass

from pyxivapi.models import Filter, Sort
client = pyxivapi.XIVAPIClient(api_key="0564745d57eb42419b7c85aef1e6c8645a577a137a2b4b4d80fe3d838c87818a")


async def getItemByName(index,name):    
    # Item search with paging
    item = await client.index_search(
        name=name,
        indexes=[index],
        columns=["*"],
        language='en',
        page=0,
        per_page=10
    )
    await client.session.close()   
    print(item)
    return item['Results'][0]

async def getItemById(index,id):
    
    item = await client.index_by_id(
        index=index,
        content_id=id,
        columns=["*"],
        language="en"
    )    
    await client.session.close()
    print(item)
    return item




if __name__ == '__main__':   
    #load_dotenv()  # This line brings all environment variables from .env into os.environ
    #print("Chave xivapi_key", os.environ['xivapi_key']) 
    #logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    loop = asyncio.get_event_loop()
    item = Item(loop.run_until_complete(getItemByName("Recipe","Indagator's Helmet of Gathering")))
    print(f"Encontrado {item.UrlType} {item.ID} - {item.Name}")
    recipeClass = loop.run_until_complete(getItemById("Item",item.ID))    
    recipeClass = RecipeClass(recipeClass["Recipes"][0])
    #rever esse classjob pq preciso desse id
    #classJob =loop.run_until_complete(getItemById("ClassJob",recipeClass.ID))
    print(f"O item {item.Name} é uma {item.UrlType} com ID: {recipeClass.ID} ")

    #teste = loop.run_until_complete(getItemById("Recipe",item.ID))
    # for x in range(10):
    #     nome = teste[f"item_ingredient{x}"]
    #     if(nome): print(nome)
    



   
    