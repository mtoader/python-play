from piston.handler import BaseHandler
from piston.utils import rc, require_mime, FormValidationError
from todo.api.forms import ListForm, ItemForm
from todo.models import List, Item


class ListHandler(BaseHandler):

    model = List
    fields = ('id', 'name')
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def read(self, request, list_id=None):
        """
        Returns a single post if `list_id` is given,
        otherwise a subset.
        
        """

        try:
            if list_id:
                return List.objects.get(user = request.user, pk=list_id)
            else:
                return List.objects.filter(user = request.user)
        except Exception as e:
           return rc.NOT_FOUND

    @require_mime('json', 'yaml')
    def create(self, request):
        form = ListForm(request.data)

        if not form.is_valid():
            raise FormValidationError(form)

        list = List.objects.create(user = request.user, name = request.data['name'])
        list.save()
        return list

    @require_mime('json', 'yaml')
    def update(self, request, list_id=None):

        if list_id is None:
            return rc.BAD_REQUEST

        form = ListForm(request.data)

        if form.is_valid():
            raise FormValidationError(form)

        try:
            list = List.objects.filter(user = request.user).get(pk=list_id)
            list.name = request.data['name']
            list.save()
        except Exception:
            return rc.NOT_FOUND

        return list

    def delete(self, request, list_id=None):
        if list_id is None:
            return rc.BAD_REQUEST

        try:
            list = List.objects.filter(user = request.user).get(pk=list_id)
            list.delete()
            return rc.DELETED
        except Exception:
            return rc.NOT_FOUND
        
class ItemHandler(BaseHandler):

    model = List
    fields = ('id', 'text', 'due_on', 'started_on', 'completed', )
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def read(self, request, list_id=None, item_id=None):
        """
        Returns a single post if `list_id` is given,
        otherwise a subset.

        """
        
        if list_id is None:
            return rc.BAD_REQUEST

        try:
            list = List.objects.filter(user = request.user).get(pk=list_id)

            if item_id:
                return Item.objects.filter(list = list).get(pk=item_id)
            else:
                return Item.objects.filter(list = list)
        except Exception as e:
           return rc.NOT_FOUND

    @require_mime('json', 'yaml')
    def create(self, request, list_id=None):

        if list_id is None:
            return rc.BAD_REQUEST

        form = ItemForm(request.data)

        if not form.is_valid():
            raise FormValidationError(form)

        try:
            list = List.objects.filter(user = request.user).get(pk=list_id)

            item = Item.objects.create(request.data)
            item.list = list
            item.save()
            return item
        
        except Exception:
            return rc.NOT_FOUND


    @require_mime('json', 'yaml')
    def update(self, request, list_id=None, item_id=None):

        if list_id is None or item_id is None:
            return rc.BAD_REQUEST

        form = ListForm(request.data)

        if form.is_valid():
            raise FormValidationError(form)

        try:
            list = List.objects.filter(user = request.user).get(pk=list_id)
            item = Item.objects.filter(list = list).get(pk=item_id)
            item.text = request.data['text']
            item.save()
        except Exception:
            return rc.NOT_FOUND

        return list

    def delete(self, request, list_id=None, item_id=None):

        if list_id is None or item_id is None:
            return rc.BAD_REQUEST

        try:
            list = List.objects.filter(user = request.user).get(pk=list_id)
            item = Item.objects.filter(list = list).get(pk=item_id)
            item.delete()
            return rc.DELETED
        except Exception:
            return rc.NOT_FOUND

