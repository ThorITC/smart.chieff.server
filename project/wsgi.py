import os, sys
sys.path.append('/var/www/smartchief.loc/project')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartchief.settings")

application = get_wsgi_application()
