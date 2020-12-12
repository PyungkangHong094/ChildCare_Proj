from django.test import TestCase
import unittest
# from unittest import TestCase
from .forms import ApplicationForm
from .models import Application
from django.core.files.temp import NamedTemporaryFile

# Create your tests here.
########## Sujeong Youn ###########

class TestApplicationForm(unittest.TestCase):

    def test_valid_form(self):

        temp_file = NamedTemporaryFile(suffix='.pdf')
        title = "Here is a title"
        content = "Here is content"
        data = {'title': title, 'content': content, 'attached_file': temp_file.name}
        print(data)
        form = ApplicationForm(data=data)
        self.assertTrue(form.is_valid())

# <MultiValueDict: {'attached_file': [<InMemoryUploadedFile: Article Summary No.2.pdf (application/pdf)>]}>

    # def test_invalid_form(self):
    #     w = Appllication.objects.create(title='Foo', body='')
    #     data = {'title': w.title, 'body': w.body,}
    #     form = ApplicationForm(data=data)
    #     self.assertFalse(form.is_valid())


########### Ji Won Choi ###########
from django.test import TestCase
from .models import *
from django.utils import timezone
import json
from unittest import TestCase
#Test 1
class MessageTest(TestCase):

    def create_message(self, sender_id="6S", receiver_id="13P", message_content="Hello, I am a sitter. Looking for a job"):
        return Message.objects.create(sender_id=sender_id, receiver_id=receiver_id, message_content=message_content, sent_date=timezone.now())

    def test_message_creation(self):
        m = self.create_message()
        self.assertTrue(isinstance(m, Message))

#Test 2
class ReivewTest(TestCase):

    def create_review(self, rating=5, reviewer_id="6S", reviewed_user_id="13P", review_content="I really liked the service!", after_service= "True"):
        return Review.objects.create(rating=rating, reviewer_id=reviewer_id, reviewed_user_id=reviewed_user_id, review_content=review_content, after_service=after_service)

    def test_review_creation(self):
        r = self.create_review()
        self.assertTrue(isinstance(r, Review))

# class MyCalcTest(unittest.TestCase):
#     def setUp(self):
#         print("1. Executing the setUp method")
#         self.fixture = { 'a' : 1 }

#     def tearDown(self):
#         print("3. Executing the tearDown method")
#         self.fixture = None

#     def test_fixture(self):
#         print("2. Executing the test_fixture method")
#         self.assertEqual(self.fixture['a'], 1)


########### Pyunkang Hong ###########