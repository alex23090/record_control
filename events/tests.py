from django.test import TestCase
from django.urls import resolve, reverse
from .models import Event
from core.models import User, Worker, Client
from .views import events, createEvent, deleteEvent, updateEvent, eventsApproval, timetable, calendarDay
from django.test import Client as Cl
from .forms import ClientEventForm, WorkerEventForm, DateForm


class TestModels(TestCase):

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

        self.event = Event.objects.create(
            client=self.client,
            worker=self.worker,
            date='2043-03-03',
            start_time='16:00',
            end_time='17:00'
        )
        self.client_browser.login(username='johndoe', password='testpass123')

    def test_events(self):
        response = self.client_browser.get(reverse('events-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/events.html')

    def test_create_event(self):
        response = self.client_browser.get(reverse('create-event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

        response = self.client_browser.get(reverse('create-event', args=[f'{self.user_1.id}', '03-03-2030']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

    def test_update_event(self):
        response = self.client_browser.get(reverse('update-event', args=[f'{self.event.id}']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_form.html')

    def test_delete_event(self):
        response = self.client_browser.get(reverse('delete-event', args=[f'{self.event.id}']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/delete-template.html')

    def test_events_approval(self):
        response = self.client_browser.get(reverse('events-approval'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/events-approval.html')

    def test_timetable(self):
        response = self.client_browser.get(reverse('calendar', args=[f'{self.user_1.id}', 2023, 'March']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/calendar.html')

    def test_calendarDay(self):
        response = self.client_browser.get(reverse('day', args=[f'{self.user_1.id}', 2023, 'March', 3]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/day.html')


class TestForms(TestCase):

    def setUp(self):
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

    def test_client_event_form_valid_data(self):
        form = ClientEventForm(data={
            'worker': self.worker.user,
            'date': '2030-03-03',
            'start_time': '08:00'
        })
        self.assertTrue(form.is_valid())

    def test_client_event_form_no_data(self):
        form = ClientEventForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_worker_event_form_valid_data(self):
        form = WorkerEventForm(data={
            'client': self.client.user,
            'date': '2030-03-03',
            'start_time': '08:00'
        })
        self.assertTrue(form.is_valid())

    def test_worker_event_form_no_data(self):
        form = WorkerEventForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_date_form_valid_data(self):
        form = DateForm(data={'date': '2030-03-03'})
        self.assertTrue(form.is_valid())

    def test_date_form_no_data(self):
        form = DateForm(data={})
        self.assertTrue(form.is_valid())
