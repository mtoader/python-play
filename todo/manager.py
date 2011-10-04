from todo.models import List, Item

__author__ = 'Toader Mihai Claudiu (mtoader@gmail.com)'

class ToDoManager:

    def newList(self, user, listName):
        list = List(user = user, name = listName)
        list.save()
        
        return list

    def findLists(self, user):
        return List.objects.filter(user = user)

    def removeLists(self):
        List.objects.all().delete()

    def clear(self):
        Item.objects.all().delete()
        List.objects.all().delete()

    def newItem(self, list, item):
        item.list = list
        item.save()