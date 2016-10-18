from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from api.serializers import DishSerializer, DishIngredientSerializer
from chiefparser.models import Dish, DishIngredient

class RandomRecipeView(APIView):

    def get(self, request, format=None):
        try:
            dish = Dish().random_dish()
            if dish == None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ingredients = DishIngredientSerializer(DishIngredient.objects.filter(dish_id=dish.id), many=True).data
            dish_data = DishSerializer(dish, many=False).data
            return Response({'dish': dish_data, 'ingredients': ingredients})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeListView(APIView):

    def get(self, request, format=None):
        try:
            ingredients = request.query_params.get('ingredients')
            if ingredients == None:
                return Response({'message': 'Query params cann\'t equals null'}, status=status.HTTP_400_BAD_REQUEST)
            chains = DishIngredient()
            dishes = chains.get_chains(ingredients.split(','))
            return Response(DishSerializer(dishes, many=True).data)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            pass
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeView(APIView):
    def get(self, request, format=None):
        try:
            dish_id = request.query_params.get('id')
            if dish_id == None:
                return Response({'message': 'Query params cann\'t equals null'}, status=status.HTTP_400_BAD_REQUEST)
            recipe = Dish.objects.get(id=dish_id)
            ingredients = DishIngredient.objects.filter(dish_id=dish_id)
            return Response({'recipe': DishSerializer(recipe, many=False).data, 'ingredients': DishIngredientSerializer(ingredients, many=True).data})
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeSearchView(APIView):
    def get(self, request, format=None):
        try:
            search_query = request.query_params.get('search')
            dishes = Dish().search_dish(search_query)
            if not dishes == None:
                return Response(DishSerializer(dishes, many=True).data)
            return Response(None)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RatingView(APIView):

    def put(self, request, format=None):
        try:
            dish_id = int(request.query_params.get('id', ''))
            event = int(request.query_params.get('rate', ''))
            dish = Dish.objects.get(id=dish_id)
            return Response({'result': dish.rate(event), 'dish': DishSerializer(dish, many=False).data})
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
