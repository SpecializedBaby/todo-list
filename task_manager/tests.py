from django.test import TestCase
from django.urls import reverse
from .models import Tag


class TagTests(TestCase):

    def setUp(self):
        self.tag1 = Tag.objects.create(name="Work")
        self.tag2 = Tag.objects.create(name="Personal")

    def test_tag_list_view(self):
        response = self.client.get(reverse("task_manager:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/tag_list.html")
        self.assertContains(response, self.tag1.name)
        self.assertContains(response, self.tag2.name)

    def test_tag_create_view(self):
        response = self.client.post(reverse("task_manager:tag-create"), {"name": "Urgent"})
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertEqual(Tag.objects.count(), 3)
        self.assertTrue(Tag.objects.filter(name="Urgent").exists())

    def test_tag_update_view(self):
        response = self.client.post(
            reverse("task_manager:tag-update", args=[self.tag1.id]), {"name": "Work Updated"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.name, "Work Updated")

    def test_tag_delete_view(self):
        response = self.client.post(reverse("task_manager:tag-delete", args=[self.tag1.id]))
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful deletion
        self.assertEqual(Tag.objects.count(), 1)
        self.assertFalse(Tag.objects.filter(name="Work").exists())
