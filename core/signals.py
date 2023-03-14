from django.db.models.signals import post_save
from .models import Worker, Client, Schedule
from django.conf import settings
from django.core.mail import send_mail


def updateUser(sender, instance, created, **kwargs):
    account = instance
    user = account.user
    if not created:
        user.first_name = account.name
        user.username = account.username
        user.email = account.email
        user.save()

    if account.email:
        send_mail(
            'Record Control notification.',
            f'Welcome to our service, {account.name}!',
            settings.EMAIL_HOST_USER,
            [account.email],
            fail_silently=False,
        )


def createSchedule(sender, instance, created, **kwargs):
    if created:
        Schedule.objects.create(worker=instance)


post_save.connect(updateUser, sender=Worker)
post_save.connect(updateUser, sender=Client)
post_save.connect(createSchedule, sender=Worker)
