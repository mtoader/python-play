"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import base64
from django.contrib.auth.models import User

from django.test import TestCase
from todo.manager import ToDoManager
from todo.models import Item


class TodoTest(TestCase):

    def setUp(self):
        self.manager = ToDoManager()

        self.manager.clear()
        self.user = User.objects.create_user(username = "testUser", email="testUser@email.com", password="testPass")
        self.user.is_active = True
        self.user.save()
        self.user_auth = 'Basic %s' % base64.encodestring('testUser:testPass').rstrip()

        if hasattr(self, 'init_delegate'):
              self.init_delegate()

    def tearDown(self):
        self.user.delete()

class SimpleManagerTest(TodoTest):

    def test_add_list_to_user(self):
        self.assertTrue(self.manager.findLists(self.user).count() == 0)
        self.manager.newList(self.user, "TestList")
        self.assertTrue(self.manager.findLists(self.user).count() == 1)

    def test_add_list_only_to_user(self):
        user2 = User.objects.create(username = "testUser2")

        self.assertTrue(self.manager.findLists(self.user).count() == 0)
        self.assertTrue(self.manager.findLists(user2).count() == 0)
        
        self.manager.newList(self.user, "TestList2")
        self.assertTrue(self.manager.findLists(self.user).count() == 1, "The list should be added to the proper user")
        self.assertTrue(self.manager.findLists(user2).count() == 0, "The list should be added only to the proper user")


    def test_add_item_to_list(self):
        list = self.manager.newList(self.user, "TestList")
        self.manager.newItem(list, Item(text = "Item1"))

class ApiTest(TodoTest):

    def test_api_login(self):
        response = self.client.get('/api/lists/')
        self.assertEquals(response.status_code, 401)

        response = self.client.get('/api/lists/', HTTP_AUTHORIZATION='')
        self.assertEquals(response.status_code, 401)

        response = self.client.get('/api/lists/', HTTP_AUTHORIZATION=self.user_auth)
        self.assertEquals(response.status_code, 200)

    def test_api_lists(self):
        self.manager.newList(self.user, "Test")
        response = self.client.get('/api/lists/')
        self.assertEquals(response.status_code, 401)

        response = self.client.get('/api/lists/', HTTP_AUTHORIZATION=self.user_auth)
        self.assertEquals(response.status_code, 200)
        expected = """[
    {
        "name": "Test",
        "id": 1
    }
]"""
        self.assertEquals(response.content, expected)

    def test_api_list(self):
        response = self.client.get('/api/lists/')
        self.assertEquals(response.status_code, 401)

        response = self.client.get('/api/lists/', HTTP_AUTHORIZATION=self.user_auth)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "[]")

        response = self.client.get('/api/lists/1', HTTP_AUTHORIZATION=self.user_auth)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "[]")

        self.manager.newList(self.user, "Test")

        response = self.client.get('/api/lists/1', HTTP_AUTHORIZATION=self.user_auth)
        self.assertEquals(response.status_code, 200)
        expected = """[
    {
        "name": "Test",
        "id": 1
    }
]"""
        self.assertEquals(response.content, expected)

