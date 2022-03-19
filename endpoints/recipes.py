
from optparse import Option
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from fastapi_utils.tasks import repeat_every

from auth.auth_bearer import JWTBearer
from dependency_injector.wiring import inject, Provide
from typing import List, Optional
from webscrapers.webscraper import Webscraper

from models.recipe_model import RecipeModel
from db_connections.mongo_db_connection import MongoDbConnection
from infrastructure.container import Container
from utils.urls import gottimatinn_urls

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")

@router.on_event("startup")
@repeat_every(seconds=3600 * 24, raise_exceptions=False)
@inject
async def add_recipes(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),
    scraper: Webscraper = Depends(
        Provide[Container.gottimatinn_scraper]
    )
) -> None:
    """
        Scrapes new recipes every 24 hours.
    """
    urls = gottimatinn_urls(2)
    for url in urls:
        recipe = scraper.scrape_recipe(url)
        mongo_db.safe_insert_recipe(recipe)

@router.get('/recipes', status_code=200)
@inject
async def get_recipes(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),
    pageSize: Optional[int] = Query(24, ge=1, le=64),
    page: Optional[int] = Query(1, ge=1),
    groups: Optional[List[str]] = Query(None),
    tags: Optional[List[str]] = Query(None),
    random: bool = False,
    token: str = Depends(JWTBearer(Container.auth_provider)),

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
    token: str = Depends(JWTBearer(Container.auth_provider)),

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
    token: str = Depends(JWTBearer(Container.auth_provider)),


):
    return mongo_db.get_all_groups()

@router.get('/tags', status_code=200)
@inject
async def get_tags(
    mongo_db: MongoDbConnection = Depends(
        Provide[Container.mongo_db_connection_provider]
    ),
    token: str = Depends(JWTBearer(Container.auth_provider)),
):
    return mongo_db.get_all_tags()