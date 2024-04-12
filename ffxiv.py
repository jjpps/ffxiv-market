import os
import asyncio
import logging
import json
import aiohttp
import pyxivapi
#from dotenv import load_dotenv
from Item import Item
from RecipeClass import RecipeClass
from Ingredient import Ingredient

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
    #print(item)
    if(item['Results']):
        return item['Results'][0]
    else:
        return None    
    

async def getItemById(index,id):
    
    item = await client.index_by_id(
        index=index,
        content_id=id,
        columns=["*"],
        language="en"
    )    
    await client.session.close()
    #print(item)
    return item


def recursiveSearch(ingredient:Ingredient):
    loop = asyncio.get_event_loop()
    itemToCraft = Item(loop.run_until_complete(getItemByName("Recipe",ingredient.Name)))
    if(itemToCraft):
        print(f"Encontrado item: {itemToCraft.Name} com id: {itemToCraft.ID}")
        print(itemToCraft.UrlType)
        



def main():
    loop = asyncio.get_event_loop()
    itemToCraft = Item(loop.run_until_complete(getItemByName("Item","Indagator's Helmet of Gathering")))
    print(f"Encontrado {itemToCraft.UrlType} {itemToCraft.ID} - {itemToCraft.Name}")

    recipeClass = loop.run_until_complete(getItemById("Item",itemToCraft.ID))    
    recipeClass = RecipeClass(recipeClass["Recipes"][0])
    print(f"Encontrada receita {recipeClass.ID}")    

    receitaIngrediantes = loop.run_until_complete(getItemById("Recipe",recipeClass.ID))
    
    ingredientList = []
    for x in range(10):
        ingredient = receitaIngrediantes[f"ItemIngredient{x}"]
        amountIngredient = receitaIngrediantes[f"AmountIngredient{x}"]
        if(ingredient and amountIngredient):                  
            ingredientList.append(Ingredient(ingredient['ID'],ingredient['Name'] ,amountIngredient))

    for i in ingredientList:
        print(f"Ingredient:{i.id}-{i.Name} with Quantity: {i.Amount}")
        teste = recursiveSearch(i)
        print(teste)


    



if __name__ == '__main__':
    main()       
    
            

    
    



    



   
    