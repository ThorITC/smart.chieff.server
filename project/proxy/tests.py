from django.test import TestCase
from proxy.models import Proxy
import warnings
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

# Create your tests here.
class ProxyTest(TestCase):

    def setUp(self):
        Proxy().set_proxy('189.205.81.130', 8080)

    def test_set_proxy(self):
        Proxy().set_proxy('192.168.0.1', 8080)
        self.assertEqual(2, len(Proxy.objects.all()))

    #def test_get_proxy(self):
    #    self.assertEqual(type(Proxy), type(Proxy().get_proxy()))
