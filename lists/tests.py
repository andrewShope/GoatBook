from django.test import TestCase
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):
	def test_home_page_returns_correct_html(self):
		response = self.client.get("/")
		self.assertContains(response, "<title>To-Do Lists</title>")
		self.assertContains(response, "<html>")
		self.assertContains(response, "</html>")
		self.assertTemplateUsed(response, "home.html")

class ListViewTest(TestCase):
	def test_uses_list_template(self):
		# response = self.client.get("/lists/the-only-list-in-the-world/")
		# self.assertTemplateUsed(response, "list.html")
		mylist = List.objects.create()
		response = self.client.get(f"/lists/{mylist.id}/")
		self.assertTemplateUsed(response, "list.html")

	def test_displays_only_items_for_that_list(self):
		# mylist = List.objects.create()
		# Item.objects.create(text="itemey 1", list=mylist)
		# Item.objects.create(text="itemey 2", list=mylist)
		# response = self.client.get("/lists/the-only-list-in-the-world/")
		# self.assertContains(response, "itemey 1")
		# self.assertContains(response, "itemey 2")
		correct_list = List.objects.create()
		Item.objects.create(text="itemey 1", list=correct_list)
		Item.objects.create(text="itemey 2", list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text="other list item", list=other_list)

		response = self.client.get(f"/lists/{correct_list.id}")

		self.assertContains(response, "itemey 1")
		self.assertContains(response, "itemey 2")
		self.assertNotContains(response, "other list item")

class ListAndItemModelsTest(TestCase):
	def test_saving_and_retrieving_items(self):
		mylist = List()
		mylist.save()

		first_item = Item()
		first_item.text = "The first (ever) list item"
		first_item.list = mylist
		first_item.save()

		second_item = Item()
		second_item.text = "Item the second"
		second_item.list = mylist
		second_item.save()

		saved_list = List.objects.get()
		self.assertEqual(saved_list, mylist)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_item.text, first_saved_item.text)
		self.assertEqual(first_saved_item.list, mylist)
		self.assertEqual(second_item.text, second_saved_item.text)
		self.assertEqual(second_saved_item.list, mylist)

class NewListTest(TestCase):
	def test_can_save_a_POST_request(self):
		self.client.post("/lists/new", data={"item_text": "A new list item"})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.get()
		self.assertEqual(new_item.text, "A new list item")

	def test_redirects_after_POST(self):
		response = self.client.post("/lists/new", data={"item_text": "A new list item"})
		self.assertRedirects(response, "/lists/the-only-list-in-the-world/")