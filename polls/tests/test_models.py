from django.test import TestCase, RequestFactory
from django.test import Client
from ..models import Person, Team
from django.contrib.auth.models import AnonymousUser, User
from ..views import person_list
from django.urls import reverse


class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.create(name='Jan', shirt_size='L')
        Person.objects.create(name="Bruce", shirt_size='L')
        cls.client = Client()
        cls.login = User.objects.create_user(
            username='patryk', email='panpabiel@gmail.com', password='server123')

    def test_first_name_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_first_name_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field('name').max_length
        self.assertEqual(max_length, 60)

    def test_person_id(self):
        person = Person.objects.get(id=1)
        person_id = person.id
        self.assertEqual(person_id, 1)

    def test_person_details(self):
        self.client.login(username='patryk', password='server123')
        url = reverse('person-persons')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Team.objects.create(name='As Monaco', country='FR')

    def test_team_name_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_team_name_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)
