from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from todo.api.handlers import ListHandler, ItemHandler


class CsrfExemptResource(Resource):
      """A Custom Resource that is csrf exempt"""
      def __init__(self, handler, authentication=None):
          super(CsrfExemptResource, self).__init__(handler, authentication)
          self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

auth = HttpBasicAuthentication(realm='ToDoApplication')

list_handler = CsrfExemptResource(ListHandler, authentication=auth)
item_handler = CsrfExemptResource(ItemHandler, authentication=auth)

urlpatterns = patterns('',
   url(r'^lists/(?P<list_id>[^/]+)/items/(?P<item_id>[^/]+)/', item_handler),
   url(r'^lists/(?P<list_id>[^/]+)/items/', item_handler),
   url(r'^lists/(?P<list_id>[^/]+)/', list_handler),
   url(r'^lists/', list_handler),
)