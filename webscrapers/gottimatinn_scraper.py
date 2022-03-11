from typing import TYPE_CHECKING, Dict, List
from bs4 import BeautifulSoup

from webscrapers.if_scraper import IfScraper

class GottimatinnScraper(IfScraper):

    def scrape(self, page_source: BeautifulSoup) -> Dict:
        recipe = {}
    
        name = page_source.find('h1', {'class': 'hdln--recipe'})
        if name and len(name) == 1: recipe['name'] = name.text
        

        image_url = page_source.find('div', {'class': 'hero__img-container'}).find('img')
        if image_url and image_url.has_attr('src'): recipe['image_url'] = 'https://www.gottimatinn.is/' + image_url['src']

        description = page_source.select_one('#body_section > section.section--tint.section--recipe.text-center.mt-md-6.pb-md-0.text-md-left > div > div > div.col-lg-5.offset-lg-1.pt-4.pt-lg-7.pb-0 > div.row.text-left > div > p')
        
        recipe['description'] = description.text if description else None

        serving_size = self.__get_recipe_size(page_source)
    
        ingredients_container = page_source.find('div', {'class': 'recipe__ingredients'})
        if ingredients_container:
            ingredients = self.__get_ingredients(ingredients_container, serving_size["amount"])
        recipe["ingredients"] = ingredients
        
        recipe["instructions"] = self.__get_instructions(page_source)

        recipe["tags"] = [tag.text for tag in page_source.find_all('a', {'class': 'button button--small mr-2 mb-2'})]        
        
        author = page_source.select_one('#body_section > section.mt-5.mt-md-7.pb-5.pb-md-6.recipe > div > div > div.col-md-7.offset-md-1.recipe__content > p > strong')
        if author: recipe["author"] = author.text

        recipe["website"] = 'https://www.gottimatinn.is/'
        return recipe
    
    def __get_instructions(self, html: BeautifulSoup) -> List[dict]:
        recipe_container = html.find('div', {'class': 'recipe__content'})
        headings = recipe_container.find_all('h2')
        lists = recipe_container.find_all('ul')

        steps = []
        for heading in headings:
            if 'aðferð' not in heading.text.lower() and heading.text != "":
                steps.append(heading.text)

        instructions = []

        if len(steps) == 0 or len(steps) != len(lists):
            res = {}
            res["title"] = 'Aðferð'
            res['steps'] = [li.text.replace(".\n", " ").replace("\n", "").strip() for li in recipe_container.find_all('li')]
            instructions.append(res)
            return instructions
        
        for index, step in enumerate(steps):
            res = {}
            res['title'] = step
            res['steps'] = []
            list = lists[index]
            for li in lists:
                res['steps'].append(li.text.replace(".\n", " ").replace("\n", "").strip())
            instructions.append(res)

        return instructions

        

    
    def __get_recipe_size(self, html: BeautifulSoup) -> dict:
        span = html.find('span', {'class': 'recipe__multiplier'})
        amount = int(span['data-amount']) if span['data-amount'].isdigit() else 1
        res =  {'amount': amount, 'unit': span['data-unit'], 'unit_singular': span['data-unit-singular']}
        return res

    def __get_ingredients(self, ingredients_container: BeautifulSoup, serving_multiplier: int) -> dict:
        tables = ingredients_container.find_all('table', {'class': 'recipe__ingredient-list'})
        headings = ingredients_container.find_all('h2')
        
        steps = []
        for heading in headings:
            #Trying to get all the relevant headings, for each steps
            if 'innihald' not in heading.text.lower() and heading.text != '':
                steps.append(heading.text)
        
        #extracting ingredients from steps
        ingredients = []
        if len(steps) == 0 or len(steps) != len(tables):
            #There is just one step
            res = {}
            res["step_name"] = ""
            res["items"] = []
            rows = ingredients_container.find_all('tr')
            for row in rows:
                res["items"].append(self.__extract_ingredients(row, serving_multiplier))
            ingredients.append(res)
            return ingredients

        if len(tables) == len(steps):
            for index, step in enumerate(steps):
                res = {}
                res["step_name"] = step
                res["items"] = []
                rows = tables[index].find_all('tr')
                for row in rows:
                    res["items"].append(self.__extract_ingredients(row, serving_multiplier))
                ingredients.append(res)
        return ingredients
    
    def __extract_ingredients(self, row: BeautifulSoup, serving_multiplier) -> dict:
        columns = row.find_all('td')
        data_amount = None
        data_unit = None
        if columns[0].has_attr('data-amount') and columns[0].has_attr('data-unit'):
            data_amount = columns[0]['data-amount']
            data_amount = float(data_amount) * serving_multiplier
            data_unit = columns[0]['data-unit']
        res = {'qty': str(data_amount) + " " +str(data_unit), 'ingredient': columns[1].text}
        return res