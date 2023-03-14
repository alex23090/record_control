from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Notification
from django.core.paginator import Paginator


@login_required(login_url='/accounts/login/')
def inbox(request):
    if request.method == 'POST':
        notification_ids = request.POST.getlist('notification_id')
        Notification.objects.filter(id__in=notification_ids).delete()
        if len(notification_ids) == 1:
            messages.success(request, "You successfully deleted notification!")
            return redirect('inbox')
        elif len(notification_ids) > 1:
            messages.success(request, "You successfully deleted notifications!")
            return redirect('inbox')
    searched = request.GET.get('searched', False)
    try:
        if searched:
            n = Notification.objects.filter(receiver=request.user.id).filter(Q(initiator__username__contains=searched)
                                                                             | Q(content__contains=searched)).order_by('-timestamp')
            print(n)
        else:
            n = Notification.objects.filter(receiver=request.user.id).order_by('-timestamp')
    except:
        n = None

    new = len([i for i in n if not i.is_read])

    p = Paginator(n, 8)
    page = request.GET.get('page')
    n = p.get_page(page)
    elided_range = list(p.get_elided_page_range())

    context = {'notifications': n, 'searched': searched,  'elided_range': elided_range, 'new_notifications': new}
    return render(request, 'inbox/inbox.html', context)


@login_required(login_url='/accounts/login/')
def notification(request, id):
    n = Notification.objects.get(id=id)
    if not n.is_read:
        n.is_read = True
        n.save()
    new = len(Notification.objects.filter(is_read=False, receiver=request.user.id))
    context = {'notification': n, 'new_notifications': new}
    return render(request, 'inbox/notification.html', context)
