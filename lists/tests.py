from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST">')
        self.assertRegex(
            response.content.decode(),
            r'<input[^>]*name\s*=\s*["\']item_text["\']',
        )

    def test_can_save_a_POST_request(self):
        response = self.client.post(
            "/", data={"item_text": "A new list item"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")
        self.assertRedirects(response, "/")

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        first_item = Item.objects.create(text="first item")
        second_item = Item.objects.create(text="second item")
        response = self.client.get("/")
        self.assertContains(response, first_item.text)
        self.assertContains(response, second_item.text)



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
        self.assertEqual(
            first_saved_item.text, "The first (ever) list item"
        )
        self.assertEqual(second_saved_item.text, "Item the second")
