from django.db import models
from django.utils import timezone
from datetime import datetime
import json
from django.db.models import Count

# Create your models here.
class DishType(models.Model):

    class Meta:
        db_table = 'dish_type'

    type_name = models.CharField(max_length=250)

    def create_dish_type(self,type_name):
        try:
            return DishType.objects.get(type_name=type_name)
        except:
            self.type_name = type_name
            self.save()
            return self


class DishCountry(models.Model):

    class Meta:
        db_table = 'dish_country'

    country_name = models.CharField(max_length=255)
    logo_name = models.CharField(max_length=255, null=True)
    logo_cdn_url = models.CharField(max_length=255, null=True)

    def create_dish_country(self,country_name):
        if country_name == None:
            return None
        try:
            return DishCountry.objects.get(country_name=country_name)
        except:
            self.country_name = country_name
            self.save()
            return self


class EnergyValue(models.Model):

    class Meta:
        db_table = 'energy_value'

    calorific = models.CharField(max_length=150, null=True)
    proteins = models.CharField(max_length=150, null=True)
    fats = models.CharField(max_length=150, null=True)
    carbohydrates = models.CharField(max_length=150, null=True)
    comment = models.TextField(null=True)


class Ingredient(models.Model):

    class Meta:
        db_table = 'ingredient'

    name = models.CharField(max_length=150)
    logo_name = models.CharField(max_length=255, null=True)
    logo_cdn_url = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    def create_ingredient(self, name):
        try:
            ingredient = Ingredient.objects.get(name=name)
            return ingredient
        except:
            self.name = name
            self.save()
            return self


    def update_ingredient(self, name, logo=None, description=None):
        try:
            ingredient = self.create_ingredient(name)
            ingredient.logo_cdn_url = logo
            ingredient.description = description
            ingredient.save()
            return ingredient
        except:
            pass

    @staticmethod
    def get_popular_ingredients():
        try:
            first_twenty = DishIngredient.objects.values('ingredient').annotate(ingredients_count=Count('ingredient')).order_by('-ingredients_count')[:20]
            first_twenty = [ingredient['ingredient'] for ingredient in first_twenty]
            return Ingredient.objects.filter(pk__in=first_twenty)
        except:
            return None

    @staticmethod
    def search_ingredient(query):
        try:
            return Ingredient.objects.filter(name__icontains=query)
        except:
            return None


class Rating(models.Model):

    class Meta:
        db_table = 'rating'

    likes = models.IntegerField()
    dislikes = models.IntegerField()

    #def __init__(self, likes=0, dislikes=0):
    #    super(Rating, self).__init__()
    #    self.likes = likes
    #    self.dislikes = dislikes

    def get_ratio(self):
        try:
            one_percent = (self.likes + self.dislikes)/100.0
            return int(round(100.0 - self.dislikes/one_percent)) if not one_percent == 0 else 0
        except:
            return 0


class Dish(models.Model):

    class Meta:
        db_table = 'dish'

    timezone.now()
    uid = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255)
    dish_type = models.ForeignKey(DishType)
    dish_country = models.ForeignKey(DishCountry, null=True)
    energy_val = models.ForeignKey(EnergyValue, null=True)
    portions = models.IntegerField()
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    rating = models.ForeignKey(Rating)
    cooking_time = models.CharField(max_length=255, null=True)
    recipe = models.TextField(null=False)
    logo_name = models.CharField(max_length=255, null=True)
    logo_cdn_url = models.CharField(max_length=255, null=True)
    comment = models.TextField(null=True)

    def random_dish(self):
        return Dish.objects.order_by('?').first()

    def create_dish(self, uid, name, dish_type, country, portions, time, recipe, comment=None):
        '''
        name - string
        dish_type - string
        country - string
        energy_val - dict
        portions - string/number
        time - string
        recipe - string
        '''
        try:
            return Dish.objects.get(uid=uid)
        except:
            self.uid = uid
            self.name = name
            self.dish_type = DishType().create_dish_type(dish_type)
            self.dish_country = DishCountry().create_dish_country(country)
            self.portions = portions
            self.rating = Rating.objects.create(likes=0, dislikes=0)
            self.cooking_time = time
            self.recipe = self.__recipe_agregator(recipe)
            self.save()
            return self

    def search_dish(self, query):
        try:
            return Dish.objects.filter(name__icontains=query)
        except:
            return None

    def rate(self, rate_value):
        try:
            if rate_value == 1:
                self.__like()
            else:
                self.__dislike()
            return True
        except:
            return False

    def __recipe_agregator(self, recipe):
        return json.dumps(recipe, ensure_ascii=False)

    def __like(self):
        self.rating.likes += 1
        self.rating.save()
        self.save()

    def __dislike(self):
        self.rating.dislikes += 1
        self.rating.save()
        self.save()

class DishIngredient(models.Model):
    class Meta:
        db_table = 'dish_ingredient'

    dish = models.ForeignKey(Dish)
    ingredient = models.ForeignKey(Ingredient)
    volume = models.CharField(max_length=250)

    def create_chain(self, dish, ingredient, volume):
        try:
            return DishIngredient.objects.get(dish=dish, ingredient=ingredient, volume=volume)
        except:
            self.dish = dish
            self.ingredient = ingredient
            self.volume = volume
            self.save()
            return self

    def get_chains(self, chain_array):
        chains = DishIngredient.objects.filter(ingredient_id__in=chain_array)
        dishes = dict()
        for chain in chains:
            if not chain.dish_id in dishes:
                dishes[chain.dish_id] = 1
            else:
                dishes[chain.dish_id] +=1
        result_list = list()
        for dish in dishes:
            if dishes[dish] == len(chain_array):
                result_list.append(dish)
        return Dish.objects.filter(id__in=result_list)
