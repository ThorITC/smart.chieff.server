from rest_framework import serializers
from chiefparser.models import Dish, Ingredient, DishIngredient, Rating,\
                              DishType, DishCountry

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('likes', 'dislikes')


class DishCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DishCountry
        fields = ('country_name', 'logo_cdn_url')


class DishTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishType
        field = 'type_name'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'logo_cdn_url')


class DishIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False, read_only=False)
    class Meta:
        model = DishIngredient
        fields = ('volume', 'ingredient')


class DishSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(many=False)
    dish_type = DishTypeSerializer(many=False)
    dish_country = DishCountrySerializer(many=False)
    class Meta:
        model = Dish
        fields = ('id', 'name', 'logo_cdn_url', 'portions', 'cooking_time', 'recipe', 'rating', 'dish_type', 'dish_country')
