from django.test import TestCase
from .models import Client, Worker, Schedule, User


class CustomUserTests(TestCase):

    def test_create_client(self):
        user = User.objects.create(
            username='johndoe',
            first_name='John Doe',
            email='johndoe@gmail.com',
            password='testpass123',
            is_client=True
        )

        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.first_name, 'John Doe')
        self.assertEqual(user.email, 'johndoe@gmail.com')
        self.assertEqual(user.is_client, True)

        client = Client.objects.create(
            user=user,
            name=user.first_name,
            username=user.username,
            email=user.email
        )

        self.assertEqual(client.user, user)
        self.assertEqual(client.username, 'johndoe')
        self.assertEqual(client.name, 'John Doe')
        self.assertEqual(client.email, 'johndoe@gmail.com')

    def test_create_worker(self):
        user = User.objects.create(
            username='johndoe',
            first_name='John Doe',
            email='johndoe@gmail.com',
            password='testpass123',
            is_worker=True
        )

        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.first_name, 'John Doe')
        self.assertEqual(user.email, 'johndoe@gmail.com')
        self.assertEqual(user.is_worker, True)

        worker = Worker.objects.create(
            user=user,
            name=user.first_name,
            username=user.username,
            email=user.email
        )

        self.assertEqual(worker.user, user)
        self.assertEqual(worker.username, 'johndoe')
        self.assertEqual(worker.name, 'John Doe')
        self.assertEqual(worker.email, 'johndoe@gmail.com')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@gmail.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@gmail.com')
        self.assertEqual(admin_user.is_active, True)
        self.assertEqual(admin_user.is_staff, True)
        self.assertEqual(admin_user.is_superuser, True)
