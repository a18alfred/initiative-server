from django.test import TestCase
from core.apps.projects.models import Category
from core.service import create_test_image


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.test_category = Category.objects.create(name='test_category')
        self.test_category.save()
        self.test_category2 = Category.objects.create(name='test_category2', icon=create_test_image())
        self.test_category2.save()

    def tearDown(self):
        self.test_category.delete()
        self.test_category2.delete()

    def test_category_str(self):
        """
        Тестируем __str__ модели категория
        """
        name = 'test'
        category = Category.objects.create(name=name)
        self.assertEqual(category.__str__(), name)

    def test_category_slug(self):
        """
        Тестируем автогенерацию slug модели категория
        """
        name = 'test'
        category = Category.objects.create(name=name)
        category.save()
        self.assertTrue(category.slug)

    def test_category_default_icon(self):
        """
        Тестируем дефолтную иконку после удаления иконки у категории
        """
        self.assertEqual(self.test_category.icon, 'categories/default_category_icon.png')
        self.assertNotEqual(self.test_category2.icon, 'categories/default_category_icon.png')
        self.test_category2.icon = ''
        self.test_category2.save()

        self.assertEqual(self.test_category2.icon, 'categories/default_category_icon.png')
