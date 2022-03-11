from pydantic import BaseModel, Field
from typing import List, Optional
from bson.objectid import ObjectId

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            return ""
        return str(v)

class IngredientModel(BaseModel):
    qty: Optional[str]
    ingredient: str

class IngredientStepModel(BaseModel):
    step_name: Optional[str]
    items: List[IngredientModel]

class InstructionModel(BaseModel):
    title: str
    steps: List[str]

class RecipeModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    name: str
    description: Optional[str]
    url: str
    image_url: Optional[str]
    ingredients: List[IngredientStepModel]
    instructions: List[InstructionModel]
    tags: Optional[List[str]]
    author: Optional[str]
    website: str
    groups: Optional[List[str]] = []
