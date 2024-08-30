from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):
	def test_home_page_returns_correct_html(self):
		response = self.client.get("/")
		self.assertContains(response, "<title>To-Do Lists</title>")
		self.assertContains(response, "<html>")
		self.assertContains(response, "</html>")
		self.assertTemplateUsed(response, "home.html")

	def test_can_save_a_POST_request(self):
		response = self.client.post("/", data={"item_text": "A new list item"})
		self.assertContains(response, "A new list item")
		self.assertTemplateUsed(response, "home.html")

class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = "The first (ever) list item"
		first_item.save()

		second_item = Item()
		second_item.text = "Item the second"
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_item.text, first_saved_item.text)
		self.assertEqual(second_item.text, second_saved_item.text)