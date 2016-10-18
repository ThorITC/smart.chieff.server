from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from chiefparser.models import Ingredient
from api.serializers import IngredientSerializer

class PopularIngredientsView(APIView):

    def get(self, request, format=None):
        try:
            top_ingredients = Ingredient.get_popular_ingredients()
            if top_ingredients:
                return Response(IngredientSerializer(top_ingredients, many=True).data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
