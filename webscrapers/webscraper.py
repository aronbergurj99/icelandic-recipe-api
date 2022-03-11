import requests
from bs4 import BeautifulSoup

from webscrapers.if_scraper import IfScraper
from models.recipe_model import RecipeModel
from utils.loggers import error_logger

class Webscraper:
    def __init__(self, scraper: IfScraper) -> None:
        self.__scraper = scraper

    def set_scraper(self, scraper: IfScraper) -> None:
        self.__scraper = scraper
    
    @error_logger
    def scrape_recipe(self, url) -> RecipeModel:
        page_source = BeautifulSoup(requests.get(url).text, 'html.parser')
        recipe_dict = self.__scraper.scrape(page_source)
        recipe_dict['url'] = url
        return RecipeModel(**recipe_dict)
