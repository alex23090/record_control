from django.test import TestCase
from django.test import Client as Cl
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Client, Worker, Schedule, User
from .views import home, worker_register, client_register, account, editAccount, profileView
from .forms import ClientSignUpForm, WorkerSignUpForm, WorkerAccountForm, ClientAccountForm


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='johndoe',
            first_name='John Doe',
            email='johndoe@gmail.com',
            password='testpass123',
            is_client=True,
            is_worker=True,
        )

        self.assertEqual(self.user.username, 'johndoe')
        self.assertEqual(self.user.first_name, 'John Doe')
        self.assertEqual(self.user.email, 'johndoe@gmail.com')
        self.assertEqual(self.user.is_client, True)
        self.assertEqual(self.user.is_worker, True)

    def test_create_client(self):
        client = Client.objects.create(
            user=self.user,
            name=self.user.first_name,
            username=self.user.username,
            email=self.user.email
        )

        self.assertEqual(client.user, self.user)
        self.assertEqual(client.username, 'johndoe')
        self.assertEqual(client.name, 'John Doe')
        self.assertEqual(client.email, 'johndoe@gmail.com')

    def test_create_worker(self):
        worker = Worker.objects.create(
            user=self.user,
            name=self.user.first_name,
            username=self.user.username,
            email=self.user.email
        )

        self.assertEqual(worker.user, self.user)
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

    def test_create_schedule(self):
        worker = Worker.objects.create(
            user=self.user,
            name=self.user.first_name,
            username=self.user.username,
            email=self.user.email
        )

        self.assertEqual(worker.user, self.user)
        self.assertEqual(worker.username, 'johndoe')
        self.assertEqual(worker.name, 'John Doe')
        self.assertEqual(worker.email, 'johndoe@gmail.com')

        schedule = Schedule.objects.create(
            worker=worker,
            start_time='08:00',
            end_time='17:00'
        )

        self.assertEqual(schedule.worker, worker)
        self.assertEqual(schedule.start_time, '08:00')
        self.assertEqual(schedule.end_time, '17:00')


class TestUrls(TestCase):

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_worker_signup_url(self):
        url = reverse('worker-signup')
        self.assertEqual(resolve(url).func, worker_register)

    def test_signup_url(self):
        url = reverse('client-signup')
        self.assertEqual(resolve(url).func, client_register)

    def test_account_url(self):
        url = reverse('account')
        self.assertEqual(resolve(url).func, account)

    def test_edit_account_url(self):
        url = reverse('edit-account')
        self.assertEqual(resolve(url).func, editAccount)

    def test_profile_url(self):
        url = reverse('profile', args=['1'])
        self.assertEqual(resolve(url).func, profileView)


class TestViews(TestCase):

    def setUp(self):
        self.client = Cl()
        self.user = User.objects.create_user(
            username='johndoe',
            first_name='John Doe',
            email='johndoe@gmail.com',
            password='testpass123',
            is_worker=True
        )
        self.worker = Worker.objects.create(
            user=self.user,
            name=self.user.first_name,
            username=self.user.username,
            email=self.user.email
        )
        self.client.login(username='johndoe', password='testpass123')



    def test_home_get(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/specialists.html')

    def test_worker_register_get(self):
        response = self.client.get(reverse('worker-signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/worker_signup_form.html')

    def test_client_register_get(self):
        response = self.client.get(reverse('client-signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/client_signup_form.html')

    def test_account(self):
        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account.html')

    def test_edit_account_get(self):
        response = self.client.get(reverse('edit-account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account_form.html')


    def test_profile(self):
        response = self.client.get(reverse('profile', args=[self.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile.html')


class TestForms(TestCase):

    def test_client_signup_form_valid_data(self):
        form = ClientSignUpForm(data={
            'first_name': 'John Doe',
            'email': 'doe@gmail.com',
            'username': 'johndoe',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertTrue(form.is_valid())

    def test_client_signup_form_no_data(self):
        form = ClientSignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_worker_signup_form_valid_data(self):
        form = WorkerSignUpForm(data={
            'first_name': 'John Doe',
            'email': 'doe@gmail.com',
            'username': 'johndoe',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertTrue(form.is_valid())

    def test_worker_signup_form_no_data(self):
        form = WorkerSignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_worker_account_form_valid_data(self):
        form = WorkerAccountForm(data={
            'name': 'John Doe',
            'username': 'johndoe',
            'email': 'doe@gmail.com',
            'profile_image': SimpleUploadedFile('/static/images/profiles/user-default.png', b'test content')
        })
        self.assertTrue(form.is_valid())

    def test_worker_account_form_no_data(self):
        form = WorkerAccountForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_client_account_form_valid_data(self):
        form = ClientAccountForm(data={
            'name': 'John Doe',
            'username': 'johndoe',
            'email': 'doe@gmail.com',
            'profile_image': SimpleUploadedFile('/static/images/profiles/user-default.png', b'test content'),
            'bio': "Hi, I'm backend developer!"
        })
        self.assertTrue(form.is_valid())

    def test_client_account_form_no_data(self):
        form = ClientAccountForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
