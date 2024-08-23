import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Domain
from .forms import DomainForm

class DomainViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.domain = Domain.objects.create(
            name='TestDomain',
            domain_type='FEM',
            regions='1,2',
            mesh_dimension=3,
            xmin=0.0,
            xmax=10.0,
            ymin=0.0,
            ymax=10.0,
            zmin=0.0,
            zmax=10.0,
            nx=10,
            ny=10,
            nz=10,
            element_kind='cuboid8'
        )

    def test_domain_list_view_get(self):
        response = self.client.get(reverse('domains:domain_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domains/domain_list.html')
        self.assertContains(response, 'TestDomain')
        self.assertIsInstance(response.context['form'], DomainForm)

    def test_domain_list_view_post_valid(self):
        data = {
            'name': 'NewDomain',
            'domain_type': 'FEM',
            'regions': '1,2,3',
            'mesh_dimension': 3,
            'xmin': 0.0,
            'xmax': 20.0,
            'ymin': 0.0,
            'ymax': 20.0,
            'zmin': 0.0,
            'zmax': 20.0,
            'nx': 20,
            'ny': 20,
            'nz': 20,
            'element_kind': 'cuboid27'
        }
        response = self.client.post(reverse('domains:domain_list'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Domain.objects.filter(name='NewDomain').exists())
        self.assertRedirects(response, reverse('domains:domain_list'))

    def test_domain_list_view_post_invalid(self):
        data = {
            'name': 'InvalidDomain',
            'domain_type': 'InvalidType',
            'mesh_dimension': 5,  # Invalid dimension
        }
        response = self.client.post(reverse('domains:domain_list'), data=data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertFalse(Domain.objects.filter(name='InvalidDomain').exists())
        self.assertContains(response, 'Error while adding the domain.')

    def test_domain_update_view_get(self):
        response = self.client.get(reverse('domains:edit_domain', kwargs={'pk': self.domain.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domains/edit_domain.html')
        self.assertContains(response, 'TestDomain')

    def test_domain_update_view_post_valid(self):
        data = {
            'name': 'UpdatedDomain',
            'domain_type': 'FEM',
            'regions': '1,2,3,4',
            'mesh_dimension': 2,
            'xmin': 0.0,
            'xmax': 15.0,
            'ymin': 0.0,
            'ymax': 15.0,
            'nx': 15,
            'ny': 15,
            'element_kind': 'quad4',
            'number_of_refinement_steps': 1  # Providing a value for the required field
        }
        response = self.client.post(reverse('domains:edit_domain', kwargs={'pk': self.domain.pk}), data=data)

        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.domain.refresh_from_db()  # Refresh the instance from the DB
        self.assertEqual(self.domain.name, 'UpdatedDomain')  # Verify the update was applied
        self.assertEqual(self.domain.mesh_dimension, 2)
        self.assertRedirects(response, reverse('domains:domain_list'))  # Ensure redirection is to the domain list

    def test_domain_update_view_post_invalid(self):
        data = {
            'name': 'UpdatedDomain',
            'domain_type': 'FEM',
            'regions': '1,2,3,4',
            'mesh_dimension': 5,
            'xmin': 0.0,
            'xmax': 15.0,
            'ymin': 0.0,
            'ymax': 15.0,
            'nx': 15,
            'ny': 15,
            'element_kind': 'quad4',
            'number_of_refinement_steps': 1  # Providing a value for the required field
        }
        response = self.client.post(reverse('domains:edit_domain', kwargs={'pk': self.domain.pk}), data=data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        print()
        self.assertContains(response, 'mesh_dimension: This field is required.', html=True)

    def test_domain_delete_view_get(self):
        response = self.client.get(reverse('domains:delete_domain', kwargs={'pk': self.domain.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domains/delete_domain.html')
        self.assertContains(response, 'Are you sure you want to delete')

    def test_domain_delete_view_post(self):
        response = self.client.post(reverse('domains:delete_domain', kwargs={'pk': self.domain.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Domain.objects.filter(pk=self.domain.pk).exists())
        self.assertRedirects(response, reverse('domains:domain_list'))

class DomainFormTestCase(TestCase):
    def test_domain_form_valid(self):
        form_data = {
            'name': 'TestDomain',
            'domain_type': 'FEM',
            'regions': '1,2,3',
            'mesh_dimension': 3,
            'xmin': 0.0,
            'xmax': 10.0,
            'ymin': 0.0,
            'ymax': 10.0,
            'zmin': 0.0,
            'zmax': 10.0,
            'nx': 10,
            'ny': 10,
            'nz': 10,
            'element_kind': 'cuboid8',
            'nonorthogonal_mesh': False,
            'number_of_refinement_steps': 0,
            'sanity_check': True,
            'parallel': False
        }
        form = DomainForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_domain_form_invalid_empty_name(self):
        form_data = {
            'name': '',  # Empty name
            'domain_type': 'FEM',
            'mesh_dimension': 3,
            'xmin': 0.0,
            'xmax': 10.0,
            'element_kind': 'cuboid8'
        }
        form = DomainForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_domain_form_invalid_domain_type(self):
        form_data = {
            'name': 'TestDomain',
            'domain_type': 'InvalidType',
            'mesh_dimension': 3,
            'xmin': 0.0,
            'xmax': 10.0,
            'element_kind': 'cuboid8'
        }
        form = DomainForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('domain_type', form.errors)

    def test_domain_form_invalid_mesh_dimension(self):
        form_data = {
            'name': 'TestDomain',
            'domain_type': 'FEM',
            'mesh_dimension': 5,  # Invalid dimension
            'xmin': 0.0,
            'xmax': 10.0,
            'element_kind': 'cuboid8'
        }
        form = DomainForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mesh_dimension', form.errors)

    def test_domain_form_invalid_element_kind(self):
        form_data = {
            'name': 'TestDomain',
            'domain_type': 'FEM',
            'mesh_dimension': 3,
            'xmin': 0.0,
            'xmax': 10.0,
            'element_kind': 'invalid_element'
        }
        form = DomainForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('element_kind', form.errors)

    def test_domain_form_nonorthogonal_mesh(self):
        form_data = {
            'name': 'NonorthogonalDomain',
            'domain_type': 'FEM',
            'regions': '1',
            'mesh_dimension': 3,
            'nonorthogonal_mesh': True,
            'mesh_vector1': '1.0, 0.0, 0.0',
            'mesh_vector2': '0.0, 1.0, 0.0',
            'mesh_vector3': '0.0, 0.0, 1.0',
            'element_kind': 'cuboid8'
        }
        form = DomainForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_domain_form_parallel(self):
        form_data = {
            'name': 'ParallelDomain',
            'domain_type': 'FEM',
            'regions': '1',
            'mesh_dimension': 3,
            'parallel': True,
            'xmin_p': 0.0,
            'xmax_p': 10.0,
            'ymin_p': 0.0,
            'ymax_p': 10.0,
            'zmin_p': 0.0,
            'zmax_p': 10.0,
            'num_geom_cpus': 4,
            'element_kind': 'cuboid8'
        }
        form = DomainForm(data=form_data)
        self.assertTrue(form.is_valid())

class DomainModelTestCase(TestCase):
    def test_domain_model_str(self):
        domain = Domain.objects.create(
            name='TestDomain',
            domain_type='FEM',
            regions='1,2',
            mesh_dimension=3,
            xmin=0.0,
            xmax=10.0,
            ymin=0.0,
            ymax=10.0,
            zmin=0.0,
            zmax=10.0,
            nx=10,
            ny=10,
            nz=10,
            element_kind='cuboid8'
        )
        self.assertEqual(str(domain), 'TestDomain - FEM')

    def test_domain_model_mesh_vectors(self):
        domain = Domain.objects.create(
            name='VectorDomain',
            domain_type='FEM',
            regions='1',
            mesh_dimension=3,
            nonorthogonal_mesh=True,
            mesh_vector1='1.0, 0.0, 0.0',
            mesh_vector2='0.0, 1.0, 0.0',
            mesh_vector3='0.0, 0.0, 1.0',
            element_kind='cuboid8'
        )
        self.assertEqual(domain.mesh_vector1, '1.0, 0.0, 0.0')
        self.assertEqual(domain.mesh_vector2, '0.0, 1.0, 0.0')
        self.assertEqual(domain.mesh_vector3, '0.0, 0.0, 1.0')

    def test_domain_model_parallel_settings(self):
        domain = Domain.objects.create(
            name='ParallelDomain',
            domain_type='FEM',
            regions='1',
            mesh_dimension=3,
            parallel=True,
            xmin_p=0.0,
            xmax_p=10.0,
            ymin_p=0.0,
            ymax_p=10.0,
            zmin_p=0.0,
            zmax_p=10.0,
            num_geom_cpus=4,
            element_kind='cuboid8'
        )
        self.assertTrue(domain.parallel)
        self.assertEqual(domain.xmin_p, 0.0)
        self.assertEqual(domain.xmax_p, 10.0)
        self.assertEqual(domain.num_geom_cpus, 4)