from django.test import TestCase
from django.urls import reverse
from django.utils.functional import cached_property

from drfapp.core.models import Organization, User


class BaseTest(TestCase):
    fixtures = 'initial',

    @cached_property
    def user1(self):
        return User.objects.get(name='user1')

    @cached_property
    def user2(self):
        return User.objects.get(name='user2')

    @cached_property
    def viewer1(self):
        return User.objects.get(name='viewer1')

    @cached_property
    def viewer2(self):
        return User.objects.get(name='viewer2')

    @cached_property
    def admin1(self):
        return User.objects.get(name='admin1')

    @cached_property
    def admin2(self):
        return User.objects.get(name='admin2')

    @cached_property
    def organization1(self):
        return Organization.objects.get(name='Organization 1')

    @cached_property
    def organization2(self):
        return Organization.objects.get(name='Organization 2')


class UserTestCase(BaseTest):
    def test_permissions(self):
        test_user_id = self.user1.id
        test_org_id = self.user1.organization_id
        tests = {
            # user, (GET, POST, UPDATE, DELETE)
            self.user1: (200, 403, 200, 403),
            self.user2: (403, 403, 403, 403),
            self.viewer1: (200, 403, 403, 403),
            self.viewer2: (403, 403, 403, 403),
            self.admin1: (200, 201, 200, 204),
            self.admin2: (403, 403, 403, 403),
        }
        for user, (sc_get, sc_post, sc_update, sc_delete) in tests.items():
            # get
            self.client.force_login(user)
            resp = self.client.get(reverse('api:users', args=[test_user_id]))
            self.assertEqual(resp.status_code, sc_get, user)

            # post
            self.client.force_login(user)
            resp = self.client.post(reverse('api:users'), {
                'name': 'test',
                'phone': '(555) 555-555',
                'email': f'test{user.name}@test.com',
                'organization': test_org_id,
            }, content_type='application/json')
            self.assertEqual(resp.status_code, sc_post, (user, resp.content))

            # update
            # delete


class OrganizationPermissionsTestCase(BaseTest):
    def test_organization_ifo(self):
        url = reverse('api:organizations', kwargs={
            'pk': self.organization1.id
        })
        tests = {
            self.user1: 403,
            self.user2: 403,
            self.viewer1: (200, 403),
            self.viewer2: 403,
            self.admin1: (200, 200),
            self.admin2: 403,
        }
        for user, status_code in tests.items():
            try:
                sc_get, sc_patch = status_code
            except TypeError:
                sc_get, sc_patch = status_code, status_code
            self.client.force_login(user)
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, sc_get, user)

            resp = self.client.patch(url, data={
                'name': 'test',
            }, content_type='application/json')
            self.assertEqual(resp.status_code, sc_patch, user)

    def test_user_list(self):
        url = reverse('api:organization-users', kwargs={
            'pk': self.organization1.id
        })
        tests = {
            self.user1: 403,
            self.user2: 403,
            self.viewer1: 200,
            self.viewer2: 403,
            self.admin1: 200,
            self.admin2: 403,
        }
        for user, status_code in tests.items():
            self.client.force_login(user)
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status_code, user)

    def test_user(self):
        url = reverse('api:organization-users', kwargs={
            'pk': self.organization1.id,

        })
        tests = {
            self.user1: 403,
            self.user2: 403,
            self.viewer1: 200,
            self.viewer2: 403,
            self.admin1: 200,
            self.admin2: 403,
        }
        for user, status_code in tests.items():
            self.client.force_login(user)
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status_code, user)
