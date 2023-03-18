from django.test import TestCase
from .models import Notification
from core.models import User


class NotificationTests(TestCase):

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
