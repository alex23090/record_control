from django.test import TestCase
from django.urls import reverse, resolve
from .models import Notification
from core.models import User, Worker, Client
from .views import inbox, notification
from django.test import Client as Cl


class TestModels(TestCase):

    def test_create_notification(self):
        user_1 = User.objects.create(
            username='johndoe',
            first_name='John Doe',
            email='johndoe@gmail.com',
            password='testpass123',
            is_client=True
        )

        self.assertEqual(user_1.username, 'johndoe')
        self.assertEqual(user_1.first_name, 'John Doe')
        self.assertEqual(user_1.email, 'johndoe@gmail.com')
        self.assertEqual(user_1.is_client, True)

        user_2 = User.objects.create(
            username='dennis',
            first_name='Den Ivy',
            email='denivy@gmail.com',
            password='testpass123',
            is_worker=True
        )

        self.assertEqual(user_2.username, 'dennis')
        self.assertEqual(user_2.first_name, 'Den Ivy')
        self.assertEqual(user_2.email, 'denivy@gmail.com')
        self.assertEqual(user_2.is_worker, True)

        notification = Notification.objects.create(
            content=f'{user_2.first_name} created an appointment!',
            initiator=user_2,
            receiver=user_1
        )
        self.assertEqual(notification.content, f'{user_2.first_name} created an appointment!')
        self.assertEqual(notification.initiator, user_2)
        self.assertEqual(notification.receiver, user_1)
        self.assertEqual(notification.is_read, False)


class TestUrls(TestCase):

    def test_inbox_url(self):
        url = reverse('inbox')
        self.assertEqual(resolve(url).func, inbox)

    def test_notification_url(self):
        url = reverse('notification', args=['1'])
        self.assertEqual(resolve(url).func, notification)


class TestViews(TestCase):
    def setUp(self):
        self.client_browser = Cl()
        self.user_1 = User.objects.create_user(
            username='johndoe',
            first_name='John Doe',
            email='johndoe@gmail.com',
            password='testpass123',
            is_worker=True
        )
        self.worker = Worker.objects.create(
            user=self.user_1,
            name=self.user_1.first_name,
            username=self.user_1.username,
            email=self.user_1.email
        )
        self.user_2 = User.objects.create_user(
            username='dennis',
            first_name='Den Ivy',
            email='denivy@gmail.com',
            password='testpass123',
            is_client=True
        )

        self.client = Client.objects.create(
            user=self.user_2,
            name=self.user_2.first_name,
            username=self.user_2.username,
            email=self.user_2.email
        )
        Notification.objects.create(
            content=f"{self.worker.name} created a new event on 2043-03-03 at 08:00 - 09:00",
            initiator=self.worker.user, receiver=self.client.user)
        self.client_browser.login(username='johndoe', password='testpass123')

    def test_inbox(self):
        response = self.client_browser.get(reverse('inbox'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox/inbox.html')

    def test_notifications(self):
        response = self.client_browser.post(reverse('create-event'),
                                            {'client': 'Den Ivy',
                                             'date': '2043-03-03',
                                             'start_time': '08:00'})
        response = self.client_browser.get(reverse('notification', args=[Notification.objects.get(initiator=self.user_1.id).id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox/notification.html')
