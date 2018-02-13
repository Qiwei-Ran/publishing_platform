from django.test import TestCase
from views import list_projects


# Create your tests here.

class SimpleTest(TestCase):
    # Test show_index page
    def test_show_index(self):
        response = self.client.get('/project/show_index/')
        self.assertEquals(response.status_code, 200)

