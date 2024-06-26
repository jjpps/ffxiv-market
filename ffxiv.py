import os
import asyncio
import pyxivapi
import pandas as pd
#from dotenv import load_dotenv
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
        return item
    except:
        return None
      

def recursiveSearch(itemPai):
    loop = asyncio.get_event_loop()
    itemToCraft = loop.run_until_complete(getItemByName("Recipe",itemPai.Name))
    if(itemToCraft):        
        if(itemToCraft["UrlType"] == "Recipe"):            
            receitaIngrediantes = loop.run_until_complete(getItemById("Recipe",itemToCraft["ID"]))

            itemPai.Receita = []
            for x in range(10):
                ingredientFilho = receitaIngrediantes[f"ItemIngredient{x}"]
                amountIngredientFilho = receitaIngrediantes[f"AmountIngredient{x}"]                
                Icon = receitaIngrediantes[f"Icon"]

                if(ingredientFilho and amountIngredientFilho):                                        
                    itemPai.Receita.append(Ingredient(ingredientFilho["ID"],ingredientFilho["Name"],amountIngredientFilho,Icon,"ItemFilho"))

            return itemPai

        



def main(item):    
    data=[]
    loop = asyncio.get_event_loop()
    itemToCraft = loop.run_until_complete(getItemByName("Item",item))  

    recipeClass = loop.run_until_complete(getItemById("Recipe",itemToCraft["ID"]))    
    if(recipeClass is None):
        recipeClass = loop.run_until_complete(getItemById("Item",itemToCraft["ID"]))
       
    recipeClass = recipeClass["Recipes"][0]
    receitaIngrediantes = loop.run_until_complete(getItemById("Recipe",recipeClass["ID"]))
    data.append({"ID":itemToCraft["ID"],"Name":itemToCraft["Name"],"Type":"ItemToCraft","Amount":1,"Icon":None})
    ingredientList = []
    for x in range(10):
        ingredient = receitaIngrediantes[f"ItemIngredient{x}"]
        amountIngredient = receitaIngrediantes[f"AmountIngredient{x}"]
        if(ingredient and amountIngredient):
            ingredientList.append(Ingredient(ingredient['ID'],ingredient['Name'] ,amountIngredient))

    for i in ingredientList:
        i.Type = "ItemPai"
        i.Receita = None
        recursiveSearch(i)
    
    
    for itemPai in ingredientList:
        if (itemPai.Receita is None):
            data.append({"ID":itemPai.id,"Name":itemPai.Name,"Type":itemPai.Type,"Amount":itemPai.Amount,"Icon":itemPai.Icon})
        
        if(itemPai.Receita is not None):            
            for receita in itemPai.Receita:               
                data.append({"ID":receita.id,"Name":receita.Name,"Type":receita.Type,"Amount":receita.Amount*itemPai.Amount,"Icon":receita.Icon})
        else:            
            data.append({"ID":itemPai.id,"Name":itemPai.Name,"Type":itemPai.Type,"Amount":itemPai.Amount,"Icon":itemPai.Icon})    
    os.system('cls')    
    return data
    

        
        
        



    



if __name__ == '__main__':
    itemList =[]    
    columns=['ID','Name','Type','Amount','Icon','InventoryAmount','AmountLeft']
    data=[]
    
    var = str(input("Item to Search Separeted By ,(comma): "))
    var = var.split(',')    
    for i in var:
        data += main(i)
    
    
    df = pd.DataFrame(data, columns=columns)
    print(df)
    var = None
    if(len(data)>1):
        var =df.groupby(["ID","Name","Type"]).sum(["Amount","Type"])
    else:
        var = df.groupby(["ID","Name"]).sum(["Amount","Type"])
    var.sort_values(by="Name",ascending=False).to_excel("crafting.xlsx")



    
    
            

    
    



    



   
    