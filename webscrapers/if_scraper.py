from abc import ABC, abstractmethod
from models.recipe_model import RecipeModel
from bs4 import BeautifulSoup

class IfScraper(ABC):
    @abstractmethod
    def scrape(page_source: BeautifulSoup, url) -> RecipeModel:
        pass