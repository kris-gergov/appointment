from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import ExtendedUserCreationForm, UserProfileForm, MeetingForm, EditBookingSlotsForm
from django.contrib import messages
from .models import Meeting
from datetime import datetime
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
import datetime as dt
import calendar
from django.urls import reverse
from django.utils.safestring import mark_safe
from .utils import EventCalendar
from django.http import Http404


# Create your views here.

@login_required()
def home(request):
    if not request.user.is_superuser:
        after_day = request.GET.get('meeting_date__gte', None)
        extra_context = {}

        if not after_day:
            d = dt.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = dt.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = dt.date.today()

        previous_month = dt.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - dt.timedelta(days=1)  # backs up a single day
        previous_month = dt.date(year=previous_month.year, month=previous_month.month,
                                 day=1)  # find first day of previous month

        last_day = calendar.monthrange(d.year, d.month)
        next_month = dt.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + dt.timedelta(days=1)  # forward a single day
        next_month = dt.date(year=next_month.year, month=next_month.month,
                             day=1)  # find first day of next month

        extra_context['previous_month'] = reverse('home') + '?meeting_date__gte=' + str(
            previous_month)
        extra_context['next_month'] = reverse('home') + '?meeting_date__gte=' + str(next_month)

        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, request.user, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return render(request, 'authentication/home.html', extra_context)
    else:
        logout(request)
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:  # if user exists
            login(request, user)
            messages.success(request, 'Successful login!')
            return redirect('home')
        else:
            messages.success(request, 'Error: Incorrect login details!')
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})


@login_required()
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():  # Validate both forms
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)  # log user in
            login(request, user)

            messages.success(request, 'Successful registration!')
            return redirect('home')
    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'authentication/register.html', context)


@login_required()
def user_profile(request):
    if request.user.profile.user_type == "adviser":
        user = request.user
        context = {'user': user}
        return render(request, 'authentication/user_profile.html', context)
    else:
        return redirect('home')


@login_required()
def change_slots(request):
    if request.user.profile.user_type == "adviser":  # only advisers can edits their slots
        if request.method == 'POST':
            profile_form = EditBookingSlotsForm(request.POST, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile has been changed!')
                return redirect('home')
        else:
            profile_form = EditBookingSlotsForm(instance=request.user.profile)
    else:
        return redirect('home')

    context = {'profile_form': profile_form}
    return render(request, 'authentication/change_slots.html', context)


@login_required()
def meeting(request):
    if request.user.profile.user_type == "student":  # only students can create meetings
        if request.method == 'POST':
            meeting_form = MeetingForm(request.POST, user=request.user)

            if meeting_form.is_valid():
                meeting_instance = meeting_form.save(commit=False)
                meeting_instance.meeting_student = request.user  # assign correct variables before saving
                meeting_instance.meeting_adviser = request.user.profile.adviser
                meeting_instance.save()

                meeting_title = meeting_form.cleaned_data.get('meeting_title')
                meeting_description = meeting_form.cleaned_data.get('meeting_description')
                meeting_student_name = meeting_instance.meeting_student.profile.__str__()
                meeting_date = meeting_form.cleaned_data.get('meeting_date')
                meeting_time = meeting_form.cleaned_data.get('meeting_slot')

                subject = 'Meeting requested from ' + meeting_student_name
                message = 'Meeting date: {} at {} \n ' \
                          'Meeting title: {} \n ' \
                          'Meeting description: {} \n ' \
                          'Please confirm or cancel the meeting.'.format(meeting_date, meeting_time, meeting_title,
                                                                         meeting_description)
                email_from = settings.EMAIL_HOST_USER  # meeting_instance.meeting_student.email
                recipient_list = [meeting_instance.meeting_adviser.email, ]
                # send_mail(subject, message, email_from, recipient_list)

                messages.success(request, 'Meeting created!')
                return redirect('home')
        else:
            meeting_form = MeetingForm(user=request.user)
    else:
        return redirect('home')

    context = {'form': meeting_form}
    return render(request, 'authentication/meeting.html', context)


@login_required()
def meeting_detail_(request, pk):
    try:
        meeting = Meeting.objects.get(pk=pk)
    except Meeting.DoesNotExist:
        raise Http404('Meeting does not exist')

    return render(request, 'authentication/meeting_detail.html', {'meeting': meeting})


@login_required()
def unconfirmed_meeting_list(request):
    if request.user.profile.user_type == "student":
        queryset = Meeting.objects.filter(meeting_student=request.user)  # student meetings
    else:
        queryset = Meeting.objects.filter(meeting_adviser=request.user)  # adviser meetings
    queryset = queryset.filter(confirmed=False).filter(meeting_date__gt=datetime.now()).order_by('meeting_date')
    context = {"meeting_list": queryset}
    return render(request, 'authentication/unconfirmed_meetings.html', context)


@login_required()
def confirmed_meeting_list(request):
    if request.user.profile.user_type == "student":
        queryset = Meeting.objects.filter(meeting_student=request.user)
    else:
        queryset = Meeting.objects.filter(meeting_adviser=request.user)
    queryset = queryset.filter(confirmed=True).filter(meeting_date__gt=datetime.now()).order_by('meeting_date')
    context = {"meeting_list": queryset}
    return render(request, 'authentication/confirmed_meetings.html', context)


@login_required()
def past_meeting_list(request):
    if request.user.profile.user_type == "student":
        queryset = Meeting.objects.filter(meeting_student=request.user)
    else:
        queryset = Meeting.objects.filter(meeting_adviser=request.user)
    queryset = queryset.filter(confirmed=True).filter(meeting_date__lt=datetime.now()).order_by('meeting_date')
    context = {"meeting_list": queryset}
    return render(request, 'authentication/past_meetings.html', context)


@login_required()
def confirm_specific_meeting(request, pk):
    confirm_meeting = Meeting.objects.get(pk=pk)
    confirm_meeting.confirmed = True
    confirm_meeting.save()

    subject = 'Meeting confirmed!'
    message = 'Meeting date: {} at {} \n ' \
              'Meeting title: {} \n ' \
              'Meeting description: {} \n ' \
              'This meeting has been confirmed. ' \
              'Please inform your adviser if you cannot attend'.format(confirm_meeting.meeting_date,
                                                                       confirm_meeting.meeting_slot,
                                                                       confirm_meeting.meeting_title,
                                                                       confirm_meeting.meeting_description)
    email_from = settings.EMAIL_HOST_USER  # confirm_meeting.meeting_adviser.email
    recipient_list = [confirm_meeting.meeting_student.email, ]
    # send_mail(subject, message, email_from, recipient_list)

    if request.user.profile.user_type == "student":
        queryset = Meeting.objects.filter(meeting_student=request.user)
    else:
        queryset = Meeting.objects.filter(meeting_adviser=request.user)
    queryset = queryset.filter(confirmed=False).filter(meeting_date__gt=datetime.now()).order_by('meeting_date')
    context = {"meeting_list": queryset}
    return render(request, 'authentication/unconfirmed_meetings.html', context)


@login_required()
def unconfirm_specific_meeting(request, pk):
    unconfirm_meeting = Meeting.objects.get(pk=pk)
    unconfirm_meeting.confirmed = False
    unconfirm_meeting.save()

    subject = 'Meeting cancelled!'
    message = 'Meeting date: {} at {} \n ' \
              'Meeting title: {} \n ' \
              'Meeting description: {} \n ' \
              'This meeting has been cancelled. ' \
              'Please inform your adviser if you cannot attend'.format(unconfirm_meeting.meeting_date,
                                                                       unconfirm_meeting.meeting_slot,
                                                                       unconfirm_meeting.meeting_title,
                                                                       unconfirm_meeting.meeting_description)
    email_from = settings.EMAIL_HOST_USER  # confirm_meeting.meeting_adviser.email
    recipient_list = [unconfirm_meeting.meeting_student.email, ]
    # send_mail(subject, message, email_from, recipient_list)

    if request.user.profile.user_type == "student":
        queryset = Meeting.objects.filter(meeting_student=request.user)
    else:
        queryset = Meeting.objects.filter(meeting_adviser=request.user)
    queryset = queryset.filter(confirmed=True).filter(meeting_date__gt=datetime.now()).order_by('meeting_date')
    context = {"meeting_list": queryset}
    return render(request, 'authentication/confirmed_meetings.html', context)


@login_required()
def cancel_specific_meeting(request, pk):
    delete_meeting = Meeting.objects.get(pk=pk)

    subject = 'Meeting cancelled!'
    message = 'Meeting date: {} at {} \n ' \
              'Meeting title: {} \n ' \
              'Meeting description: {} \n ' \
              'This meeting has been cancelled. '.format(delete_meeting.meeting_date,
                                                         delete_meeting.meeting_slot,
                                                         delete_meeting.meeting_title,
                                                         delete_meeting.meeting_description)
    email_from = settings.EMAIL_HOST_USER  # delete_meeting.meeting_adviser.email
    recipient_list = [delete_meeting.meeting_student.email, ]
    # send_mail(subject, message, email_from, recipient_list)

    delete_meeting.delete()

    if request.user.profile.user_type == "student":
        queryset = Meeting.objects.filter(meeting_student=request.user)
    else:
        queryset = Meeting.objects.filter(meeting_adviser=request.user)
    queryset = queryset.filter(confirmed=False).filter(meeting_date__gt=datetime.now()).order_by('meeting_date')
    context = {"meeting_list": queryset}
    return render(request, 'authentication/unconfirmed_meetings.html', context)
