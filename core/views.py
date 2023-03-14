from django.shortcuts import render, redirect
from .forms import WorkerSignUpForm, ClientSignUpForm, ClientAccountForm, WorkerAccountForm
from .models import Client, Worker, User, Schedule
from django.contrib import messages
from django.contrib.auth import login
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from inbox.models import Notification


def home(request):
    searched = request.GET.get('searched', False)
    if searched:
        specialists = Worker.objects.filter(Q(name__contains=searched) | Q(username__contains=searched))
    else:
        specialists = Worker.objects.all().order_by('name')

    # Pagination
    p = Paginator(specialists, 4)
    page = request.GET.get('page')
    specialists = p.get_page(page)
    elided_range = list(p.get_elided_page_range())

    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))

    context = {'specialists': specialists, 'searched': searched, 'elided_range': elided_range, 'new_notifications': new}
    return render(request, 'core/specialists.html', context)


def client_register(request):
    form = ClientSignUpForm(request.POST)

    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, 'Client account was created!')

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'account/client_signup_form.html', context)


def worker_register(request):
    form = WorkerSignUpForm(request.POST)

    if request.method == 'POST':
        form = WorkerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, 'Worker account was created!')

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'account/worker_signup_form.html', context)


@login_required(login_url='/accounts/login/')
def account(request):
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    profile = None
    schedule = None
    if request.user.is_client:
        profile = Client.objects.get(user=request.user)
    elif request.user.is_worker:
        profile = Worker.objects.get(user=request.user)
        schedule = profile.schedule_set.get()
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {'account': profile, 'schedule': schedule, 'current_year': current_year, 'current_month': current_month, 'new_notifications': new}
    return render(request, 'core/account.html', context)


@login_required(login_url='/accounts/login/')
def editAccount(request):
    form = None
    if request.user.is_client:
        account = request.user.client
        form = ClientAccountForm(instance=account)
        if request.method == 'POST':
            form = ClientAccountForm(request.POST, request.FILES, instance=account)
            if form.is_valid():
                request.user.username = form.cleaned_data['username']
                form.save()
                messages.success(request, "Client account was successfully edited!")
                return redirect('account')
    elif request.user.is_worker:
        account = request.user.worker
        form = WorkerAccountForm(instance=account)
        if request.method == 'POST':
            form = WorkerAccountForm(request.POST, request.FILES, instance=account)
            if form.is_valid():
                request.user.username = form.cleaned_data['username']
                form.save()
                messages.success(request, "Worker account was successfully edited!")
                return redirect('account')
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {'form': form, 'new_notifications': new}
    return render(request, 'core/account_form.html', context)


def profileView(request, pk):
    current_month = None
    current_year = datetime.now().year
    schedule = None
    try:
        profile = Worker.objects.get(user_id=pk)
        current_month = datetime.now().strftime('%B')
        schedule = profile.schedule_set.get()
    except:
        profile = Client.objects.get(user_id=pk)
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {'profile': profile, 'schedule': schedule, 'current_year': current_year, 'current_month': current_month, 'new_notifications': new}
    return render(request, 'core/profile.html', context)
