import pymongo
from typing import List
from models.recipe_model import RecipeModel

class MongoDbConnection:
    def __init__(self, uri: str, db: str):
        self.client = self.__initialize(uri, db)

    def __initialize(self, uri, db) -> pymongo.MongoClient:
        client = pymongo.MongoClient(uri)
        return client[db]

    def insert_many_recipes(self, recipes: List[RecipeModel]) -> None:
        self.client["recipes"].insert_many(recipes)
    
    def insert_recipe(self, recipe: RecipeModel) -> None:
        self.client["recipes"].update_one({'url': recipe.url},{'$set': recipe.dict()}, upsert=True)