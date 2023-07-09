from django.shortcuts import render, redirect
from datetime import timedelta, date, datetime
import datetime as dt
from .models import Event
from core.models import Worker, Client, Schedule
from django.core.exceptions import ObjectDoesNotExist
from .forms import ClientEventForm, WorkerEventForm, DateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .utils import EventFormValidation, ScheduleCalendar
import calendar
from inbox.models import Notification


@login_required(login_url='/accounts/login/')
def calendarDay(request, specialist_id, year, month, day):
    requested_date = datetime(year, list(calendar.month_name).index(month), day)
    searched = request.GET.get('searched', False)
    if request.user.is_worker and request.user.worker.user_id == specialist_id and searched:
        events = Event.objects.filter(worker=specialist_id, date=requested_date.date()).filter(Q(client__name__contains=searched)
                                                                         | Q(client__username__contains=searched))
    else:
        events = Event.objects.filter(worker=specialist_id, date=requested_date.date())
    worker = Worker.objects.get(user_id=specialist_id)
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {
        'year': year,
        'month': month,
        'day': day,
        'specialist': worker,
        'events': events,
        'date': requested_date.date(),
        'searched': searched,
        'new_notifications': new,
    }
    return render(request, 'events/day.html', context)


@login_required(login_url='/accounts/login/')
def timetable(request, specialist_id, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    today = datetime.now().day

    months = list(calendar.month_name)
    months.pop(0)

    next_year = year
    previous_year = year

    try:
        next_month = months[month_number+1-1]
    except IndexError:
        next_month = months[0]
        next_year = year + 1
    if month_number-2 < 0:
        previous_month = months[11]
        previous_year = year - 1
    else:
        previous_month = months[month_number - 2]

    cal = ScheduleCalendar().formatmonth(year, month_number)

    days = calendar.monthcalendar(year, month_number)

    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))

    context = {
        'year': year,
        'month': month,
        'month_number': month_number,
        'today': today,
        'days': days,
        'next_month': next_month,
        'previous_month': previous_month,
        'calendar': cal,
        'next_year': next_year,
        'previous_year': previous_year,
        'specialist_id': specialist_id,
        'current_month': datetime.now().strftime('%B'),
        'current_year': datetime.now().year,
        'new_notifications': new,
    }
    return render(request, 'events/calendar.html', context)


@login_required(login_url='/accounts/login/')
def events(request):
    searched = request.GET.get('searched', False)
    d = request.GET.get('date', False)
    occasions = None

    if request.user.is_client:
        if searched and d:
            occasions = Event.objects.filter(client__user=request.user, date=d).filter(
                Q(worker__name__contains=searched)
                | Q(worker__username__contains=searched)).order_by('date', 'start_time', '-approved')
        elif searched:
            occasions = Event.objects.filter(client__user=request.user).filter(
                Q(worker__name__contains=searched)
                | Q(worker__username__contains=searched)).order_by('date', 'start_time', '-approved')
        elif d:
            occasions = Event.objects.filter(client__user=request.user, date=d).order_by('date', 'start_time', '-approved')
        else:
            occasions = Event.objects.filter(client__user=request.user).order_by('date', 'start_time', '-approved')
    elif request.user.is_worker:
        if searched and d:
            occasions = Event.objects.filter(worker__user=request.user, date=d).filter(
                Q(client__name__contains=searched)
                | Q(client__username__contains=searched)).order_by('date', 'start_time', '-approved')
        elif searched:
            occasions = Event.objects.filter(worker__user=request.user).filter(
                Q(client__name__contains=searched)
                | Q(client__username__contains=searched)).order_by('date', 'start_time', '-approved')
        elif d:
            occasions = Event.objects.filter(worker__user=request.user, date=d).order_by('date', 'start_time',
                                                                                         '-approved')
        else:
            occasions = Event.objects.filter(worker__user=request.user).order_by('date', 'start_time', '-approved')

    p = Paginator(occasions, 4)
    page = request.GET.get('page')
    occasions = p.get_page(page)

    elided_range = list(p.get_elided_page_range())

    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))

    context = {'events': occasions, 'searched': searched, 'elided_range': elided_range, 'new_notifications': new, 'value_date': d, 'date_form': True}
    return render(request, 'events/events.html', context)


@login_required(login_url='/accounts/login/')
def eventsApproval(request):
    h_date = date.today()
    searched = request.GET.get('searched', False)
    d = request.GET.get('date', False)
    if searched and d:
        events = Event.objects.filter(worker=request.user.worker, date=d).filter(Q(client__name__contains=searched)
            | Q(client__username__contains=searched)).order_by('-approved')
    elif searched:
        events = Event.objects.filter(worker=request.user.worker).filter(Q(client__name__contains=searched)
                                                                         | Q(client__username__contains=searched)).order_by('-approved')
    elif d:
        events = Event.objects.filter(worker=request.user.worker, date=d).order_by('-approved')
    else:
        events = Event.objects.filter(worker=request.user.worker, date=date.today()).order_by('-approved')

    if d:
        h_date = datetime.strptime(d, '%Y-%m-%d')
        h_date = h_date.strftime('%d %B %Y')

    if request.method == "POST":
        if 'form2' in request.POST:
            id_list = request.POST.getlist('boxes')

            changed = False

            for event in events:
                if str(event.id) in id_list and not event.approved:
                    Event.objects.filter(id=event.id).update(approved=True)
                    n = Notification.objects.create(
                        content=f"{event.worker.name} approved your event on {event.date} at {event.start_time} - {event.end_time}",
                        initiator=event.worker.user, receiver=event.client.user)
                    changed = True
                elif str(event.id) not in id_list and event.approved:
                    Event.objects.filter(id=event.id).update(approved=False)
                    changed = True
            if changed:
                messages.success(request, "Event list approval was successfully updated!")
            return redirect('events-list')
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {'events': events, 'searched': searched, 'new_notifications': new, 'value_date': d, 'date_form': True, 'date': h_date}
    return render(request, 'events/events-approval.html', context)


@login_required(login_url='/accounts/login/')
def createEvent(request, worker_id=None, when=None):
    page = 'create'
    events = Event.objects.all()
    if request.user.is_worker:
        worker = Worker.objects.get(user=request.user)
        if when:
            form = WorkerEventForm({'date': when})
        else:
            form = WorkerEventForm()

        if request.method == 'POST':
            form = WorkerEventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.worker = worker
                event.approved = True
                future_time = dt.datetime(1970, 1, 1, event.start_time.hour, event.start_time.minute,
                                          event.start_time.second, event.start_time.microsecond) + timedelta(hours=1)
                event.end_time = dt.time(future_time.hour, future_time.minute, future_time.second,
                                         future_time.microsecond)
                try:
                    e = Event.objects.get(date=event.date, start_time=event.start_time, worker=event.worker)
                except ObjectDoesNotExist:
                    e = False
                try:
                    x = Event.objects.get(date=event.date, start_time=event.start_time, client=event.client)
                except ObjectDoesNotExist:
                    x = False
                schedule = Schedule.objects.get(worker=worker)
                if EventFormValidation(request, events, event, schedule, x, e, page):
                    n = Notification.objects.create(
                        content=f"{worker.name} created a new event on {event.date} at {event.start_time} - {event.end_time}",
                        initiator=event.worker.user, receiver=event.client.user)
                    return redirect('events-list')
    elif request.user.is_client:
        client = Client.objects.get(user=request.user)
        if worker_id and when:
            form = ClientEventForm({'worker': worker_id, 'date': when})
        else:
            form = ClientEventForm()

        if request.method == 'POST':
            form = ClientEventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.client = client
                future_time = dt.datetime(1970, 1, 1, event.start_time.hour, event.start_time.minute,
                                          event.start_time.second, event.start_time.microsecond) + timedelta(hours=1)
                event.end_time = dt.time(future_time.hour, future_time.minute, future_time.second,
                                         future_time.microsecond)
                try:
                    e = Event.objects.get(date=event.date, start_time=event.start_time, worker=event.worker)
                except ObjectDoesNotExist:
                    e = False
                try:
                    x = Event.objects.get(date=event.date, start_time=event.start_time, client=event.client)
                except ObjectDoesNotExist:
                    x = False
                schedule = Schedule.objects.get(worker=event.worker)
                if EventFormValidation(request, events, event, schedule, x, e, page):
                    n = Notification.objects.create(
                        content=f"{client.name} created a new event on {event.date} at {event.start_time} - {event.end_time}",
                        initiator=event.client.user, receiver=event.worker.user)
                    return redirect('events-list')
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {
        'form': form,
        'new_notifications': new,
    }
    return render(request, 'events/event_form.html', context)


@login_required(login_url='/accounts/login/')
def updateEvent(request, pk):
    page = 'update'
    events = Event.objects.all()
    if request.user.is_worker:
        worker = request.user.worker
        event = worker.event_set.get(id=pk)
        form = WorkerEventForm(instance=event)

        if request.method == 'POST':
            form = WorkerEventForm(request.POST, instance=event)
            event = worker.event_set.get(id=pk)
            if form.is_valid():
                try:
                    e = Event.objects.filter(~Q(id=event.id), date=form.cleaned_data['date'],
                                             start_time=form.cleaned_data['start_time'],
                                             client=form.cleaned_data['client'])
                except ObjectDoesNotExist:
                    e = False
                try:
                    x = Event.objects.filter(~Q(id=event.id), date=form.cleaned_data['date'],
                                             start_time=form.cleaned_data['start_time'],
                                             worker=event.worker)
                except ObjectDoesNotExist:
                    x = False
                schedule = Schedule.objects.get(worker=event.worker)
                if EventFormValidation(request, events, form, schedule, x, e, page, event):
                    Event.objects.filter(id=pk).update(end_time=(
                                datetime.combine(date.today(), form.cleaned_data['start_time']) + timedelta(
                            hours=1)).time(), start_time=(
                                datetime.combine(date.today(), form.cleaned_data['start_time'])).time(), date=form.cleaned_data['date'])
                    n = Notification.objects.create(
                        content=f"{worker.name} changed an event on {event.date} at {event.start_time} - {event.end_time}",
                        initiator=event.worker.user, receiver=event.client.user)
                    return redirect('events-list')
                else:
                    return redirect('events-list')
    elif request.user.is_client:
        client = request.user.client
        event = client.event_set.get(id=pk)
        form = ClientEventForm(instance=event)

        if request.method == 'POST':
            form = ClientEventForm(request.POST, instance=event)
            event = client.event_set.get(id=pk)
            if form.is_valid():
                try:
                    e = Event.objects.filter(~Q(id=event.id), date=form.cleaned_data['date'],
                                                               start_time=form.cleaned_data['start_time'],
                                                               client=event.client)
                except ObjectDoesNotExist:
                    e = False
                try:
                    x = Event.objects.filter(~Q(id=event.id), date=form.cleaned_data['date'],
                                                               start_time=form.cleaned_data['start_time'],
                                                               worker=form.cleaned_data['worker'])
                except ObjectDoesNotExist:
                    x = False
                schedule = Schedule.objects.get(worker=event.worker)
                if EventFormValidation(request, events, form, schedule, x, e, page, event):
                    Event.objects.filter(id=pk).update(end_time=(
                                datetime.combine(date.today(), form.cleaned_data['start_time']) + timedelta(
                            hours=1)).time(), start_time=(
                                datetime.combine(date.today(), form.cleaned_data['start_time'])).time(), date=form.cleaned_data['date'], approved=False)
                    n = Notification.objects.create(
                        content=f"{client.name} changed an event on {event.date} at {event.start_time} - {event.end_time}",
                        initiator=event.client.user, receiver=event.worker.user)
                    return redirect('events-list')
                else:
                    return redirect('events-list')
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {
        'form': form,
        'new_notifications': new,
    }
    return render(request, 'events/event_form.html', context)


@login_required(login_url='/accounts/login/')
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        event.delete()
        if request.user.is_worker:
            n = Notification.objects.create(
                content=f"{event.worker.name} deleted an event on {event.date} at {event.start_time} - {event.end_time}",
                initiator=event.worker.user, receiver=event.client.user)
        elif request.user.is_client:
            n = Notification.objects.create(
                content=f"{event.client.name} deleted an event on {event.date} at {event.start_time} - {event.end_time}",
                initiator=event.client.user, receiver=event.worker.user)
        messages.success(request, "Event was successfully deleted!")
        return redirect('events-list')


    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {'event': event, 'new_notifications': new}
    return render(request, 'events/delete-template.html', context)
