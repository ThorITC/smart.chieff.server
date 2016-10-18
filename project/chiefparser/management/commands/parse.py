from django.core.management.base import BaseCommand, CommandError
from chiefparser.models import Dish, Ingredient, DishIngredient
from http import client
import json
import requests
from bs4 import BeautifulSoup
import time
from multiprocessing.dummy import Pool
import warnings
import socket
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')


class StaticHelper(object):
    @staticmethod
    def check_to_connect():
        try:
            socket.gethostbyaddr('www.yandex.ru')
        except socket.gaierror:
            return False
        return True

    @staticmethod
    def get_proxy():
        try:
            conn = client.HTTPConnection('gimmeproxy.com')
            conn.request("GET", '/api/getProxy?get=true&post=true&protocol=http')
            document = json.loads(conn.getresponse().read().decode("utf-8"))
            conn.close()
            return {key: document[key] for key in set(['ip', 'port']) & set(document.keys())}
        except:
            return False


class Command(BaseCommand):
    args = 'Name of services'
    help = 'Command to start parse'

    def handle(self, *args, **options):
        if not len(args) == 0:
            if args[0] == 'ingredients':
                IngredientParser()
            elif args[0] == 'proxy':
                print(StaticHelper.get_proxy())

        else:
            print('hui')
            #DishParser()




class IngredientParser(object):
    """docstring for """
    def __init__(self):
        super().__init__()
        self.__ingredient_parse_starter()

    def __ingredient_parse_starter(self):
        try:
            ingredient_categories_list = self.__parse_ingredient_category_links()
            if ingredient_categories_list == 404:
                raise NameError('Unknown result of operation')
            for category in ingredient_categories_list:
                self.__parse_ingredients_in_category(category)
        except:
            print('Error!')

    def __parse_ingredient_category_links(self):
        try:
            if not StaticHelper.check_to_connect():
                self.__parse_ingredient_category_links()
            r = requests.get('http://eda.ru/wiki')
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                main_div = soup.findAll('div', {'class': 'g-one-col s-sticky-position-scroll-place'})[0]
                ingredients_categories = main_div.findAll('a', {'class': 'b-list-item__link'})
                result_list = list()
                for a in ingredients_categories:
                    result_list.append(a['href'])
                return result_list
        except:
            return 404

    def __parse_ingredients_in_category(self, category_link):
        try:
            if not StaticHelper.check_to_connect():
                self.__parse_ingredients_in_category(category_link)
            page = 1
            while True:
                r = requests.get(category_link + '/page{}'.format(page))
                if not r.status_code == 200:
                    return
                ingredients = BeautifulSoup(r.text, 'html.parser')
                ingredients = ingredients.findAll('h2', {'class': 'b-list-title'})
                for link in ingredients:
                    self.__parse_ingredient(link.findAll('a')[0]['href'])
                page += 1
        except:
            return 404

    def __parse_ingredient(self, ingredient_link):
        try:
            if not StaticHelper.check_to_connect():
                self.__parse_ingredient(ingredient_link)
            r = requests.get(ingredient_link)
            soup = BeautifulSoup(r.text, 'html.parser')
            name = soup.findAll('h1', {'class': 'b-instrument-title'})[0].string
            logo = None
            #try:
            logo = soup.findAll('img', {'class': 'b-instrument-image'})[0]['src']
            #except:
            #    pass
            description = None
            #try:
            description = soup.findAll('p', {'class': 'b-instrument-description'})[0].string
            #except:
            #    pass
            ingredient = Ingredient().update_ingredient(name, logo, description)
            print(ingredient)
        except:
            pass


class DishParser(object):

    def __init__(self):
        super().__init__()
        self.errors = 0
        self.added = 0
        self.updated = 0
        self.__start()

    def __start(self):
        #try:
            main_pool = Pool(10)
            urls_list = main_pool.map(self.__get_links_to_recipe, range(1, 1775))
            main_pool.close()
            main_pool.join()
            print('Parsed %s' % str(len(urls_list)))
            for sub_list in urls_list:
                self.__analyze_links_array(sub_list)
            print('Finished!')
        #except:
        #    print('Error in dish parser')

    def __analyze_links_array(self, links_array):
        try:
            for href in links_array:
                self.__get_dish_recipe(href)
            print('Total added: %s' % str(self.added))
            print('Total errors: %s' % str(self.errors))
        except:
            pass

    def __get_links_to_recipe(self, page=1):
        try:
            if not StaticHelper.check_to_connect():
                self.__get_links_to_recipe(page)
            conn = client.HTTPSConnection('eda.ru')
            conn.request("GET", '/recepty/page{}'.format(page))
            request = conn.getresponse()
            document = request.read()
            if request.status == 404:
                return None
            conn.close()
            return self.__parse_document(str(document))
        except:
            self.errors += 1
            return None

    def __parse_document(self, document):
        try:
            result_list = list()
            soup = BeautifulSoup(document, 'html.parser')
            result = soup.find_all('h3')
            for h3 in result:
                sub_soup = BeautifulSoup(str(h3), 'html.parser')
                hrefs = sub_soup.find_all('a')
                for href in hrefs:
                    temp = href.get('href')
                    result_list.append(temp)
            return result_list
        except:
            self.errors += 1

    def __get_dish_recipe(self, link):
        try:
            if not StaticHelper.check_to_connect():
                self.__get_dish_recipe(link)
            link_array = link.split('/')
            conn = client.HTTPSConnection(link_array[2])
            conn.request("GET", '/'+'/'.join(link_array[3:]))
            conn_data = conn.getresponse()
            document = conn_data.read()
            conn.close()
            self.__parse_dish(document)
        except:
            self.errors += 1

    def __parse_dish(self, document):
        try:
            soup = BeautifulSoup(document, 'html.parser')
            recipe_id = soup.findAll('div', {'class': 'g-hidden child-element'})[0].findAll('input', {'name': 'recipeID'})[0]['value']
            try:
                id = soup.find('a', {'class': 's-ajax-favorite-control favorite-btn-new s-tooltip'})['data-recipe-url-path']
            except:
                self.errors += 1
                return
            try:
                name = soup.findAll('h1', {'class': 'fn s-recipe-name'})[0].string
            except:
                name = None
            try:
                dish_type = soup.findAll('a', {'class': 'tag category'})[0].findAll('strong')[0].string.strip()
            except:
                dish_type = None
            try:
                cooking_time = soup.findAll('time', {'class': 'value-title'})[0].string
            except:
                cooking_time = None
            try:
                portions = soup.findAll('div', {'class': 'b-ingredients-list'})[0].\
                                        findAll('option', {'selected': "'selected'"})[0]['value']
            except:
                portions = 1
            try:
                country = soup.findAll('a', {'class': 'tag cuisine-type'})[0].\
                                findAll('strong', {'class': 'b-normal-text'})[0].string.strip()
            except:
                country = None
            try:
                ingredients_temp = soup.findAll('tr', {'class': 'ingredient'})
                ingredients = dict()
                for ingredient in ingredients_temp:
                    ingredients[ingredient.find('a').string] = ingredient.find('span').string
            except:
                ingredients = None
            try:
                recipe_list = soup.findAll('li', {'class': 'instruction'})
                recipe = list()
                for item in recipe_list:
                    item_dict = dict()
                    try:
                       item_dict['img'] = item.find('img')['src']
                    except:
                        pass
                    text = item.find('div', {'class': 'text'})
                    text.b.clear()
                    item_dict['text'] = text.get_text().strip()
                    recipe.append(item_dict)
            except:
                recipe = None
            new_dish = Dish().create_dish(id, name, dish_type, country, int(portions), cooking_time, recipe)
            try:
                for ingredient in ingredients:
                    new_ingredient = Ingredient().create_ingredient(ingredient)
                    ingredient_chain = DishIngredient().create_chain(new_dish, new_ingredient, ingredients[ingredient])
            except:
                self.errors += 1
            self.__parse_logo_link(new_dish, recipe_id)
            self.added += 1
        except:
            self.errors += 1

    def __parse_logo_link(self, dish, recipe_id):
        try:
            if not StaticHelper.check_to_connect():
                self.__parse_logo_link(dish, recipe_id)
            r = requests.post('http://eda.ru/RecipePhoto/List', data = {'recipeId': recipe_id})
            if r.status_code == 200:
                dish_data = json.loads(r.text)
                if len(dish_data) > 0:
                    dish.logo_cdn_url = dish_data[0]['img']
                    dish.save()
        except:
            self.errors += 1
