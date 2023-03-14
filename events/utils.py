from calendar import HTMLCalendar
from django.contrib import messages
from datetime import date, datetime, timedelta


class ScheduleCalendar(HTMLCalendar):
    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s"><a href="%s">%d</a></td>' % (self.cssclasses[weekday], weekday, day)


def EventFormValidation(request, events, form, schedule, x, e, page, event=None):
    obstacle = False
    if page == 'create':
        for es in events:
            if ((form.start_time < es.start_time < form.end_time) or (
                    form.start_time < es.end_time < form.end_time) or (
                        es.start_time < form.start_time and es.end_time > form.end_time)) and es.date == form.date:
                obstacle = True
        if str(form.date.weekday()) in "56":
            messages.error(request, "You can not choose weekend days!")
        elif schedule.start_time > form.start_time or schedule.end_time < form.start_time or form.start_time <= schedule.end_time < form.end_time:
            messages.error(request, "You can not choose time out of worker schedule!")
        elif form.date < date.today():
            messages.error(request, "You can not choose past dates!")
        elif form.date == date.today() and form.start_time < datetime.now().time():
            messages.error(request, "You can not choose the time that has passed!")
        elif x or e:
            messages.error(request, 'This time and date is already taken! Change it to another one.')
        else:
            if obstacle:
                messages.error(request,
                               "You can not make an appointment in this time range because it's already taken!")
            else:
                form.save()
                messages.success(request, 'Event was added successfully!')
                return True
    elif page == 'update':
        end_time = (datetime.combine(date.today(), form.cleaned_data['start_time']) + timedelta(hours=1)).time()
        for es in events:
            if (((form.cleaned_data['start_time'] < es.start_time < end_time) or (
                    form.cleaned_data['start_time'] < es.end_time < end_time) or (
                        es.start_time < form.cleaned_data['start_time'] and es.end_time > end_time)) and es.date == form.cleaned_data['date']) and es != event:
                obstacle = True
        if str(form.cleaned_data['date'].weekday()) in '56':
            messages.error(request, "You can not choose weekend days!")
        elif schedule.start_time > form.cleaned_data['start_time'] or schedule.end_time < form.cleaned_data['start_time'] or form.cleaned_data['start_time'] <= schedule.end_time < end_time:
            messages.error(request, "You can not choose time out of worker schedule!")
        elif form.cleaned_data['date'] < date.today():
            messages.error(request, "You can not choose past dates!")
        elif form.cleaned_data['date'] == date.today() and form.cleaned_data['start_time'] < datetime.now().time():
            messages.error(request, "You can not choose the time that has passed!")
        elif x or e:
            messages.error(request, 'This time and date is already taken! Change it to another one.')
        else:
            if obstacle:
                messages.error(request,
                               "You can not make an appointment in this time range because it's already taken!")
            else:
                if not (form.cleaned_data['date'] == event.date and form.cleaned_data['start_time'] == event.start_time):
                    form.save()
                    messages.success(request, 'Event was updated successfully!')
                    return True
                else:
                    return False
