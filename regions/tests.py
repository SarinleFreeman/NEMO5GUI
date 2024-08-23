import json
from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from .models import Region
from .forms import RegionForm

class RegionViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.region = Region.objects.create(
            shape='Cuboid',
            tag='Test',
            region_number=1,
            priority=1,
            min_x=0,
            min_y=0,
            min_z=0,
            max_x=10,
            max_y=10,
            max_z=10
        )

    def test_region_list_view_get(self):
        response = self.client.get(reverse('regions:region_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'regions/region_list.html')
        self.assertContains(response, 'Regions Management')
        self.assertContains(response, 'Test')  # Check if the region is in the list

    def test_region_list_view_post_valid(self):
        data = {
            'shape': 'Spheroid',
            'tag': 'NewTest',
            'region_number': 2,
            'priority': 2,
            'min_x': 0,
            'min_y': 0,
            'min_z': 0,
            'max_x': 5,
            'max_y': 5,
            'max_z': 5
        }
        response = self.client.post(reverse('regions:region_list'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Region.objects.filter(tag='NewTest').exists())

    def test_region_list_view_post_invalid(self):
            data = {
                'shape': 'InvalidShape',
                'tag': 'InvalidTest',
                'region_number': 'not a number',
                'priority': -1,
                'min_x': 10,
                'min_y': 10,
                'min_z': 10,
                'max_x': 5,
                'max_y': 5,
                'max_z': 5
            }
            response = self.client.post(reverse('regions:region_list'), data=data)
            self.assertEqual(response.status_code, 200)  # Stays on the same page
            self.assertFalse(Region.objects.filter(tag='InvalidTest').exists())
            self.assertContains(response, 'Select a valid choice. InvalidShape is not one of the available choices.')
            self.assertContains(response, 'Max values must be greater than min.')

    def test_region_update_view_get(self):
        response = self.client.get(reverse('regions:edit_region', kwargs={'pk': self.region.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'regions/edit_region.html')
        self.assertContains(response, 'Edit Region')

    def test_region_update_view_post_valid(self):
        data = {
            'shape': 'Spheroid',
            'tag': 'UpdatedTest',
            'region_number': 2,
            'priority': 2,
            'min_x': 1,
            'min_y': 1,
            'min_z': 1,
            'max_x': 11,
            'max_y': 11,
            'max_z': 11
        }
        response = self.client.post(reverse('regions:edit_region', kwargs={'pk': self.region.pk}), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.region.refresh_from_db()
        self.assertEqual(self.region.tag, 'UpdatedTest')

    def test_region_update_view_post_invalid(self):
        data = {
            'shape': 'Cuboid',
            'tag': 'UpdatedTest',
            'region_number': 2,
            'priority': 2,
            'min_x': 10,
            'min_y': 10,
            'min_z': 10,
            'max_x': 5,
            'max_y': 5,
            'max_z': 5
        }
        response = self.client.post(reverse('regions:edit_region', kwargs={'pk': self.region.pk}), data=data)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Max values must be greater than min.')

    def test_region_delete_view_get(self):
        response = self.client.get(reverse('regions:delete_region', kwargs={'pk': self.region.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'regions/delete_region.html')
        self.assertContains(response, 'Are you sure you want to delete')

    def test_region_delete_view_post(self):
        response = self.client.post(reverse('regions:delete_region', kwargs={'pk': self.region.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Region.objects.filter(pk=self.region.pk).exists())

class RegionFormTestCase(TestCase):
    def test_region_form_valid(self):
        form_data = {
            'shape': 'Cuboid',
            'tag': 'ValidTest',
            'region_number': 1,
            'priority': 1,
            'min_x': 0,
            'min_y': 0,
            'min_z': 0,
            'max_x': 10,
            'max_y': 10,
            'max_z': 10
        }
        form = RegionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_region_form_invalid(self):
        form_data = {
            'shape': 'InvalidShape',
            'tag': 'Invalid Test',
            'region_number': -1,
            'priority': 0,
            'min_x': 10,
            'min_y': 10,
            'min_z': 10,
            'max_x': 5,
            'max_y': 5,
            'max_z': 5
        }
        form = RegionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('shape', form.errors)
        self.assertIn('region_number', form.errors)
        self.assertIn('priority', form.errors)
        self.assertIn('__all__', form.errors)

class RegionModelTestCase(TestCase):
    def test_region_model_str(self):
        region = Region.objects.create(
            shape='Cuboid',
            tag='TestRegion',
            region_number=1,
            priority=1,
            min_x=0,
            min_y=0,
            min_z=0,
            max_x=10,
            max_y=10,
            max_z=10
        )
        self.assertEqual(str(region), 'TestRegion - Cuboid')

    def test_region_model_clean_valid(self):
        region = Region(
            shape='Cuboid',
            tag='TestRegion',
            region_number=1,
            priority=1,
            min_x=0,
            min_y=0,
            min_z=0,
            max_x=10,
            max_y=10,
            max_z=10
        )
        try:
            region.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_region_model_clean_invalid(self):
        region = Region(
            shape='Cuboid',
            tag='TestRegion',
            region_number=1,
            priority=0,  # Invalid priority
            min_x=10,
            min_y=10,
            min_z=10,
            max_x=5,
            max_y=5,
            max_z=5  # Invalid max values
        )
        with self.assertRaises(ValidationError):
            region.full_clean()