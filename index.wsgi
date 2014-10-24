import sae

from qtmain import wsgi

application = sae.create_wsgi_app(wsgi.application)
