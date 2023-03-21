from django.test import TestCase
from django.urls import resolve, reverse
from .models import Event
from core.models import User, Worker, Client
from .views import events, createEvent, deleteEvent, updateEvent, eventsApproval, timetable, calendarDay



class EventsTests(TestCase):

    def test_create_event(self):
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

        client = Client.objects.create(
            user=user_1,
            name=user_1.first_name,
            username=user_1.username,
            email=user_1.email
        )

        self.assertEqual(client.user, user_1)
        self.assertEqual(client.username, 'johndoe')
        self.assertEqual(client.name, 'John Doe')
        self.assertEqual(client.email, 'johndoe@gmail.com')

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

        worker = Worker.objects.create(
            user=user_2,
            name=user_2.first_name,
            username=user_2.username,
            email=user_2.email
        )

        self.assertEqual(worker.user, user_2)
        self.assertEqual(worker.username, 'dennis')
        self.assertEqual(worker.name, 'Den Ivy')
        self.assertEqual(worker.email, 'denivy@gmail.com')

        event = Event.objects.create(
            client=client,
            worker=worker,
            date='2043-03-03',
            start_time='15:00',
            end_time='16:00'
        )
        self.assertEqual(event.client, client)
        self.assertEqual(event.worker, worker)
        self.assertEqual(event.date, '2043-03-03')
        self.assertEqual(event.start_time, '15:00')
        self.assertEqual(event.end_time, '16:00')


class TestUrls(TestCase):

    def test_event_list_url(self):
        url = reverse('events-list')
        self.assertEqual(resolve(url).func, events)

    def test_create_event_url(self):
        url = reverse('create-event')
        self.assertEqual(resolve(url).func, createEvent)
        url = reverse('create-event', args=['1', '03-03-2030'])
        self.assertEqual(resolve(url).func, createEvent)

    def test_update_event_url(self):
        url = reverse('update-event', args=['1'])
        self.assertEqual(resolve(url).func, updateEvent)

    def test_delete_event_url(self):
        url = reverse('delete-event', args=['1'])
        self.assertEqual(resolve(url).func, deleteEvent)

    def test_events_approval_url(self):
        url = reverse('events-approval')
        self.assertEqual(resolve(url).func, eventsApproval)

    def test_calendar_url(self):
        url = reverse('calendar', args=['1', '2024', '03'])
        self.assertEqual(resolve(url).func, timetable)

    def test_day_url(self):
        url = reverse('day', args=['1', '2024', '03', '14'])
        self.assertEqual(resolve(url).func, calendarDay)
