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
      

def recursiveSearch(ingredient:Ingredient):
    loop = asyncio.get_event_loop()
    itemToCraft = loop.run_until_complete(getItemByName("Recipe",ingredient.Name))
    if(itemToCraft):
        #print(f"Encontrado item: {itemToCraft["Name"]} com id: {itemToCraft["ID"]} ele é {itemToCraft["UrlType"]}")
        if(itemToCraft["UrlType"] == "Recipe"):
            #print(f"{itemToCraft["Name"]} é uma Receita" )
            receitaIngrediantes = loop.run_until_complete(getItemById("Recipe",itemToCraft["ID"]))
            ingredientList = []
            for x in range(10):
                ingredient = receitaIngrediantes[f"ItemIngredient{x}"]
                amountIngredient = receitaIngrediantes[f"AmountIngredient{x}"]
                Icon = receitaIngrediantes[f"Icon"]
                if(ingredient and amountIngredient):
                    #print(f"Ingredient {ingredient['ID']} name {ingredient['Name']}")
                    ingredientList.append(Ingredient(ingredient['ID'],ingredient['Name'] ,amountIngredient,Icon))
            return ingredientList

        



def main(item):
    ItemFinal = []
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
        ItemFinal.append(recursiveSearch(i))
    
    # for item in ItemFinal:
    #     if(item): 
    #         for i in item:
    #             print(f"Name do Item {i.Name} qtd: {i.Amount} Icon:{i.Icon}")
    
    return ItemFinal
        
        


    



if __name__ == '__main__':
    #Indagator's Doublet Vest of Gathering
    itemList =[]    
    itemToCsv=[]
    haveMore = True
    while (haveMore):
        var = str(input("Item to Search: "))
        itemList.append(var)
        haveMore = True if input("Continue [Y/N] ?")=="Y" else False
    for i in itemList:
        itemToCsv.append(main(i))

    with open('Crafting.csv', 'w', newline='',) as file:
        writer = csv.writer(file)
        field = ["Name", "Amount", "Icon"]
        
        writer.writerow(field)
        for item in itemToCsv:
            if(item): 
                for i in item:
                    if(i is not None):
                        for i2 in i:
                            writer.writerow([i2.Name, i2.Amount, i2.Icon])        
    




    
    
            

    
    



    



   
    