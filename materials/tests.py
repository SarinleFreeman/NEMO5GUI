import json
from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from .models import Material
from .forms import MaterialForm

class MaterialViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.material = Material.objects.create(
            name='TestMaterial',
            tag='TestTag',
            regions='1,2',
            crystal_structure='diamond',
            doping_type='N',
            doping_density=1.0,
            charge_model='electron_core',
            doping_ionization_model='electron_core',
            doping_temperature=300,
            ionization_energy=0.5,
            doping_degeneracy=2,
            nanotube_indices=[5, 10],
            additional_params={"param1": "value1"},
            disorder_type='totally_random_dopant',
            seed=1234,
            polarization=[0.0, 0.1, 0.0],
            strain_simulation=True
        )
        

    def test_material_list_view_get(self):
        response = self.client.get(reverse('materials:material_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'materials/material_list.html')
        self.assertContains(response, 'Materials Management')
        self.assertContains(response, 'TestMaterial')  # Check if the material is in the list

    def test_material_list_view_post_valid(self):
        data = {
            'name': 'NewMaterial',
            'tag': 'NewTag',
            'regions': '1,2',
            'crystal_structure': 'diamond',
            'doping_type': 'P',
            'doping_density': 1.5,
            'charge_model': 'electron_hole',
            'doping_ionization_model': 'electron_hole',
            'doping_temperature': 300,
            'ionization_energy': 0.7,
            'doping_degeneracy': 3,
            'nanotube_indices': json.dumps([5, 10]),
            'additional_params': json.dumps({"param1": "value1"}),
            'disorder_type': 'totally_random_dopant',
            'seed': 1234,
            'polarization': json.dumps([0.0, 0.1, 0.0]),
            'strain_simulation': True
        }
        response = self.client.post(reverse('materials:material_list'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Material.objects.filter(tag='NewTag').exists())

    def test_material_list_view_post_invalid(self):
        data = {
            'name': 'InvalidMaterial',
            'tag': 'TestTag',  # Duplicate tag
            'regions': '1,2',
            'crystal_structure': 'invalid_structure',  # Invalid choice
            'doping_type': 'InvalidType',
            'doping_density': -1.0,  # Invalid value
            'charge_model': 'invalid_model',
            'doping_ionization_model': 'invalid_model',
            'doping_temperature': -100,  # Invalid value
            'ionization_energy': -0.5,  # Invalid value
            'doping_degeneracy': -2,  # Invalid value
            'nanotube_indices': json.dumps([5, 10]),
            'additional_params': json.dumps({"param1": "value1"}),
            'disorder_type': 'invalid_disorder',
            'seed': -1234,  # Invalid value
            'polarization': json.dumps([0.0, 0.1, 0.0]),
            'strain_simulation': True
        }
        response = self.client.post(reverse('materials:material_list'), data=data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertFalse(Material.objects.filter(tag='InvalidTag').exists())
        self.assertContains(response, 'Select a valid choice. invalid_structure is not one of the available choices.')

    def test_material_update_view_get(self):
        response = self.client.get(reverse('materials:edit_material', kwargs={'pk': self.material.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'materials/edit_material.html')
        self.assertContains(response, 'Edit Material')

    def test_material_update_view_post_valid(self):
        data = {
            'name': 'UpdatedMaterial',
            'tag': 'UpdatedTag',
            'regions': '1,2',
            'crystal_structure': 'zincblende',
            'doping_type': 'N',
            'doping_density': 2.0,
            'charge_model': 'electron_core',
            'doping_ionization_model': 'electron_core',
            'doping_temperature': 300,
            'ionization_energy': 1.0,
            'doping_degeneracy': 4,
            'nanotube_indices': json.dumps([5, 10]),
            'additional_params': json.dumps({"param1": "value1"}),
            'disorder_type': 'totally_random_dopant',
            'seed': 1234,
            'polarization': json.dumps([0.0, 0.1, 0.0]),
            'strain_simulation': True
        }
        response = self.client.post(reverse('materials:edit_material', kwargs={'pk': self.material.pk}), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.material.refresh_from_db()
        self.assertEqual(self.material.tag, 'UpdatedTag')

    def test_material_update_view_post_invalid(self):
        data = {
            'name': 'UpdatedMaterial',
            'tag': 'TestTag',  # Duplicate tag
            'regions': '1,2',
            'crystal_structure': 'invalid_structure',  # Invalid choice
            'doping_type': 'InvalidType',
            'doping_density': -1.0,  # Invalid value
            'charge_model': 'invalid_model',
            'doping_ionization_model': 'invalid_model',
            'doping_temperature': -100,  # Invalid value
            'ionization_energy': -0.5,  # Invalid value
            'doping_degeneracy': -2,  # Invalid value
            'nanotube_indices': json.dumps([5, 10]),
            'additional_params': json.dumps({"param1": "value1"}),
            'disorder_type': 'invalid_disorder',
            'seed': -1234,  # Invalid value
            'polarization': json.dumps([0.0, 0.1, 0.0]),
            'strain_simulation': True
        }
        response = self.client.post(reverse('materials:edit_material', kwargs={'pk': self.material.pk}), data=data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertContains(response, 'Select a valid choice. invalid_structure is not one of the available choices.')

    def test_material_delete_view_get(self):
        response = self.client.get(reverse('materials:delete_material', kwargs={'pk': self.material.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'materials/delete_material.html')
        self.assertContains(response, 'Are you sure you want to delete')

    def test_material_delete_view_post(self):
        response = self.client.post(reverse('materials:delete_material', kwargs={'pk': self.material.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Material.objects.filter(pk=self.material.pk).exists())

class MaterialFormTestCase(TestCase):
    def setUp(self):
        # Create a material with the 'TestTag' to test duplicate tag validation
        Material.objects.create(
            name='ExistingMaterial',
            tag='TestTag',
            regions='1,2',
            crystal_structure='diamond',
            doping_type='N',
            doping_density=1.0,
            charge_model='electron_core',
            doping_ionization_model='electron_core',
            doping_temperature=300,
            ionization_energy=0.5,
            doping_degeneracy=2,
            nanotube_indices=[5, 10],
            additional_params={"param1": "value1"},
            disorder_type='totally_random_dopant',
            seed=1234,
            polarization=[0.0, 0.1, 0.0],
            strain_simulation=True
        )

    def test_material_form_valid(self):
        form_data = {
            'name': 'TestMaterial',
            'tag': 'TestTag2',
            'regions': '1,2',
            'crystal_structure': 'diamond',
            'doping_type': 'N',
            'doping_density': 1.0,
            'charge_model': 'electron_core',
            'doping_ionization_model': 'electron_core',
            'doping_temperature': 300,
            'ionization_energy': 0.5,
            'doping_degeneracy': 2,
            'nanotube_indices': json.dumps([5, 10]),
            'additional_params': json.dumps({"param1": "value1"}),
            'disorder_type': 'totally_random_dopant',
            'seed': 1234,
            'polarization': json.dumps([0.0, 0.1, 0.0]),
            'strain_simulation': True
        }
        form = MaterialForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_material_form_invalid_duplicate_tag(self):
        form_data = {
            'name': 'InvalidMaterial',
            'tag': 'TestTag',  # Duplicate tag
            'crystal_structure': 'diamond',
        }
        form = MaterialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tag', form.errors)

    def test_material_form_invalid_crystal_structure(self):
        form_data = {
            'name': 'InvalidMaterial',
            'tag': 'UniqueTag',
            'crystal_structure': 'invalid_structure',  # Invalid choice
        }
        form = MaterialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('crystal_structure', form.errors)

    def test_material_form_invalid_doping_density(self):
        form_data = {
            'name': 'InvalidMaterial',
            'tag': 'UniqueTag',
            'crystal_structure': 'diamond',
            'doping_density': -1.0,  # Invalid value
        }
        form = MaterialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('doping_density', form.errors)

    def test_material_form_invalid_doping_temperature(self):
        form_data = {
            'name': 'InvalidMaterial',
            'tag': 'UniqueTag',
            'crystal_structure': 'diamond',
            'doping_temperature': -100,  # Invalid value
        }
        form = MaterialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('doping_temperature', form.errors)

    def test_material_form_invalid_ionization_energy(self):
        form_data = {
            'name': 'InvalidMaterial',
            'tag': 'UniqueTag',
            'crystal_structure': 'diamond',
            'ionization_energy': -0.5,  # Invalid value
        }
        form = MaterialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ionization_energy', form.errors)

    def test_material_form_invalid_doping_degeneracy(self):
        form_data = {
            'name': 'InvalidMaterial',
            'tag': 'UniqueTag',
            'crystal_structure': 'diamond',
            'doping_degeneracy': -2,  # Invalid value
        }
        form = MaterialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('doping_degeneracy', form.errors)

    def test_material_form_invalid_seed(self):
        form_data = {
            'name': 'InvalidMaterial',
            'tag': 'UniqueTag',
            'crystal_structure': 'diamond',
            'seed': -1234,  # Invalid value
        }
        form = MaterialForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('seed', form.errors)


class MaterialModelTestCase(TestCase):
    def test_material_model_str(self):
        material = Material.objects.create(
            name='TestMaterial',
            tag='TestTag',
            regions='1,2',
            crystal_structure='diamond',
            doping_type='N',
            doping_density=1.0,
            charge_model='electron_core',
            doping_ionization_model='electron_core',
            doping_temperature=300,
            ionization_energy=0.5,
            doping_degeneracy=2,
            nanotube_indices=[5, 10],
            additional_params={"param1": "value1"},
            disorder_type='totally_random_dopant',
            seed=1234,
            polarization=[0.0, 0.1, 0.0],
            strain_simulation=True
        )
        self.assertEqual(str(material), 'TestTag - diamond')

    def test_material_model_clean_valid(self):
        material = Material(
            name='TestMaterial',
            tag='TestTag',
            regions='1,2',
            crystal_structure='diamond',
            doping_type='N',
            doping_density=1.0,
            charge_model='electron_core',
            doping_ionization_model='electron_core',
            doping_temperature=300,
            ionization_energy=0.5,
            doping_degeneracy=2,
            nanotube_indices=[5, 10],
            additional_params={"param1": "value1"},
            disorder_type='totally_random_dopant',
            seed=1234,
            polarization=[0.0, 0.1, 0.0],
            strain_simulation=True
        )
        try:
            material.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

    def test_material_model_clean_invalid(self):
        Material.objects.create(
            name='ValidMaterial',
            tag='TestTag',  # This will cause a duplicate tag error in the next material
            regions='1,2',
            crystal_structure='diamond',
            doping_type='N',
            doping_density=1.0,
            charge_model='electron_core',
            doping_ionization_model='electron_core',
            doping_temperature=300,
            ionization_energy=0.5,
            doping_degeneracy=2,
            nanotube_indices=[5, 10],
            additional_params={"param1": "value1"},
            disorder_type='totally_random_dopant',
            seed=1234,
            polarization=[0.0, 0.1, 0.0],
            strain_simulation=True
        )

        material = Material(
            name='TestMaterial',
            tag='TestTag',  # Duplicate tag
            regions='1,2',
            crystal_structure='diamond',
            doping_type='N',
            doping_density=-1.0,  # Invalid value
            charge_model='electron_core',
            doping_ionization_model='electron_core',
            doping_temperature=-300,  # Invalid value
            ionization_energy=-0.5,  # Invalid value
            doping_degeneracy=-2,  # Invalid value
            nanotube_indices=[5, 10],
            additional_params={"param1": "value1"},
            disorder_type='totally_random_dopant',
            seed=-1234,  # Invalid value
            polarization=[0.0, 0.1, 0.0],
            strain_simulation=True
        )
        with self.assertRaises(ValidationError):
            material.full_clean()