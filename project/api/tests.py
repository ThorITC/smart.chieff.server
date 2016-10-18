from django.test import TestCase, Client
import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')
# Create your tests here.
class ApiTest(TestCase):

    def test_random_dish(self):
        client = Client()
        response = client.get('/random-recipe/')
        self.assertEqual(response.status_code, 400)

    def test_get_recipe_by_ingredients_pull(self):
        client = Client()
        self.assertEqual(client.get('/recipes/?ingredients=93,89').status_code, 200)
