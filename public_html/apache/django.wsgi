import os
import sys
#import djcelery
#djcelery.setup_loader()

path = '/home/ubuntu/cart.com/public_html/'
if path not in sys.path:
        sys.path.insert(0,'/home/ubuntu/cart.com/public_html/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'shopping_cart.settings'

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
                                                        
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
