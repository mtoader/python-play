from django.contrib import admin
from todo.models import List, Item
from piston.models import Token, Consumer, Resource, Nonce


admin.site.register(List)
admin.site.register(Item)

admin.site.register(Nonce)
admin.site.register(Resource)
admin.site.register(Consumer)
admin.site.register(Token)
