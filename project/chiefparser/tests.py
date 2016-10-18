from django.test import TestCase
from chiefparser.models import Rating, Dish, DishType,\
                               DishCountry, EnergyValue,\
                               Ingredient, DishIngredient
import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

# Create your tests here.
class RateTest(TestCase):

    def test_ratio(self):
        '''
        Ratio ratio
        '''
        like = Rating()
        self.assertEqual(like.get_ratio(), 0)


class DishTypeTest(TestCase):

    '''
    def setUp(self):
        DishType().create_dish_type('Desserts')
    '''

    def test_dish_type(self):
        '''
        DishType test
        '''
        self.assertEqual(DishType().create_dish_type('Desserts').type_name, 'Desserts')

    def test_create_def(self):
        self.assertEqual(type(DishType().create_dish_type('Desserts')), type(DishType()))


class DishCountryTest(TestCase):

    def setUp(self):
        DishCountry().create_dish_country('USA')

    def test_dish_country(self):
        self.assertEqual(DishCountry.objects.get(id=1).country_name, 'USA')


class DishTest(TestCase):

    def setUp(self):
        Dish().create_dish('Test', 'test', 'Pasta', 'Italy', 6, '15 minutes', 'Test')

    def test_dish(self):
         self.assertEqual(len(Dish.objects.all()), 1)

    def test_rating(self):
        dish = Dish.objects.get()
        dish.rate(1)
        self.assertEqual(dish.rating.likes, 1)


class IngredientTest(TestCase):

    def setUp(self):
        Ingredient().create_ingredient('Muka')

    def test_ingredient(self):
        self.assertEqual(len(Ingredient.objects.all()), 1)

class DishIngredientTest(TestCase):

    def test_chain(self):
        dish = Dish().create_dish('Test', 'test', 'Pasta', 'Italy', 6, '15 minutes', 'Test')
        ingredient = Ingredient().create_ingredient('Muka')
        self.assertEqual(type(DishIngredient().create_chain(dish, ingredient, '20')), type(DishIngredient()))
