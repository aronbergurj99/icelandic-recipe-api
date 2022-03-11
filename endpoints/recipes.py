
from optparse import Option
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from dependency_injector.wiring import inject, Provide
from typing import List, Optional

from models.recipe_model import RecipeModel
from db_connections.mongo_db_connection import MongoDbConnection
from infrastructure.container import Container

router = APIRouter()

@router.get('/recipes', status_code=200)
@inject
async def get_recipes(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),
    pageSize: Optional[int] = Query(34, ge=1, le=64),
    page: Optional[int] = Query(1, ge=1),
    groups: Optional[List[str]] = Query(None),
    tags: Optional[List[str]] = Query(None),
    random: bool = False,
):
    query = {}
    if groups:
        query["groups"] = {"$in": groups}
    if tags:
        query["tags"] = {"$in": tags}

    if random:
        result = mongo_db.get_random_recipes(pageSize, query)
    else:
        result = mongo_db.get_recipes(pageSize, page, query)
    return result

@router.get('/recipes/{id}', status_code=200)
@inject
async def get_recipes(
    id: str = Path(..., title="The recipe_id of the recipe to get"),
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),
):
    res = mongo_db.get_recipe(id)
    if not res:
        raise HTTPException(status_code=404, detail="No recipe exists with supplied ID")
    return res

@router.get('/groups', status_code=200)
@inject
async def get_groups(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),

):
    return mongo_db.get_all_groups()

@router.get('/tags', status_code=200)
@inject
async def get_tags(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    )
):
    return mongo_db.get_all_tags()