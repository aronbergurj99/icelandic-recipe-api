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

    def get_all_tags(self) -> List[str]:
        return self.client['recipes'].distinct("tags")
    
    def set_groups(self):
        recipes = self.client['recipes'].find({"groups": { "$exists":True, "$eq":[]}})
        for recipe in recipes:
            groups = self.client['groups'].find({"tags": {"$in": recipe["tags"]}})
            g = set()
            for group in groups:
                g.add(group["group"])
            recipe["groups"] = list(g)
            self.insert_recipe(recipe=RecipeModel(**recipe))
        
    def get_recipes(self, page_size:int, page: int, query: dict = {}) -> List[RecipeModel]:
        results = self.client['recipes'].find(query).skip((page - 1) * page_size).limit(page_size)

        return [RecipeModel(**res) for res in results]
    
    def get_random_recipes(self, page_size, query) -> List[RecipeModel]:
        results = self.client["recipes"].aggregate([
            {"$match": query},
            {"$sample": {"size": page_size}}
        ])
        results = [RecipeModel(**res) for res in results]
        return results