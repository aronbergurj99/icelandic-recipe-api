from pydantic import BaseModel
from typing import List, Optional

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
    _id: Optional[str]
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