import os
import asyncio
import logging
import json
import aiohttp
import pyxivapi
import csv
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
    
    try:
        item = await client.index_by_id(
            index=index,
            content_id=id,
            columns=["*"],
            language="en"
        )    
        await client.session.close()
        #print(item)
        
        return item
    except:
        return None
      

def recursiveSearch(itemPai):
    loop = asyncio.get_event_loop()
    itemToCraft = loop.run_until_complete(getItemByName("Recipe",itemPai.Name))
    if(itemToCraft):
        #print(f"Encontrado item: {itemToCraft["Name"]} com id: {itemToCraft["ID"]} ele é {itemToCraft["UrlType"]}")
        if(itemToCraft["UrlType"] == "Recipe"):            
            receitaIngrediantes = loop.run_until_complete(getItemById("Recipe",itemToCraft["ID"]))

            itemPai.Receita = []
            for x in range(10):
                ingredientFilho = receitaIngrediantes[f"ItemIngredient{x}"]
                amountIngredientFilho = receitaIngrediantes[f"AmountIngredient{x}"]                
                Icon = receitaIngrediantes[f"Icon"]

                if(ingredientFilho and amountIngredientFilho):
                    #print(f"o Item {itemPai.Name} é {itemPai.Type} de {ingredientFilho["Name"]}")                    
                    itemPai.Receita.append(Ingredient(ingredientFilho["ID"],ingredientFilho["Name"],amountIngredientFilho,ingredientFilho["Icon"],"ItemFilho"))

            return itemPai

        



def main(item):    
    loop = asyncio.get_event_loop()
    itemToCraft = loop.run_until_complete(getItemByName("Item",item))
    #print(f"Encontrado {itemToCraft["UrlType"]} {itemToCraft["ID"]} - {itemToCraft["Name"]}")

    recipeClass = loop.run_until_complete(getItemById("Recipe",itemToCraft["ID"]))    
    if(recipeClass is None):
        recipeClass = loop.run_until_complete(getItemById("Item",itemToCraft["ID"]))
       
    recipeClass = recipeClass["Recipes"][0]
    #print(f"Encontrada receita {recipeClass["ID"]}")    

    receitaIngrediantes = loop.run_until_complete(getItemById("Recipe",recipeClass["ID"]))
    
    ingredientList = []
    for x in range(10):
        ingredient = receitaIngrediantes[f"ItemIngredient{x}"]
        amountIngredient = receitaIngrediantes[f"AmountIngredient{x}"]
        if(ingredient and amountIngredient):
            ingredientList.append(Ingredient(ingredient['ID'],ingredient['Name'] ,amountIngredient))

    for i in ingredientList:        
        #ItemFinal.append(recursiveSearch(i))        
        i.Type = "ItemPai"
        i.Receita = None
        recursiveSearch(i)
    
    for itemPai in ingredientList:
        #print(f"Nome {itemPai.Name} tipo {itemPai.Type}")
        if(itemPai.Receita is not None):
            print(f"o Item {itemPai.Name} possuiu receita com qtd {itemPai.Amount}")
            for receita in itemPai.Receita:
                print(f"--{receita.Name} precisa de {receita.Amount*itemPai.Amount}")
        else:
            print(f"Item {itemPai.Name} não tem receita")

        
        
        



    



if __name__ == '__main__':
    #Indagator's Doublet Vest of Gathering
    main("Indagator's Doublet Vest of Gathering")



    
    
            

    
    



    



   
    