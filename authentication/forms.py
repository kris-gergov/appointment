from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Meeting
import datetime


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    school = forms.CharField(max_length=100, required=False)
    study_year = forms.IntegerField(required=False)
    adviser = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__user_type='adviser'), empty_label=None, required=False)

    class Meta:
        model = Profile
        fields = ('user_type', 'school', 'study_year', 'booking_slots', 'adviser')

    def clean_school(self):
        user_type = self.cleaned_data.get('user_type')
        school = self.cleaned_data.get('school')
        if user_type == 'student' and (school is None or school == ""):
            raise forms.ValidationError('This field is required.')
        return school

    def clean_study_year(self):
        user_type = self.cleaned_data.get('user_type')
        study_year = self.cleaned_data.get('study_year')
        if user_type == 'student' and (study_year is None or study_year < 1 or study_year > 4):
            raise forms.ValidationError('Please enter a valid number.')
        return study_year

    def clean_booking_slots(self):
        user_type = self.cleaned_data.get('user_type')
        booking_slots = self.cleaned_data.get('booking_slots')
        if not booking_slots and user_type == 'adviser':
            raise forms.ValidationError('This field is required.')
        return booking_slots

    def clean_adviser(self):
        user_type = self.cleaned_data.get('user_type')
        adviser = self.cleaned_data.get('adviser')
        if user_type == 'adviser':
            return None
        return adviser


class EditBookingSlotsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'booking_slots'}

    def clean_booking_slots(self):
        booking_slots = self.cleaned_data.get('booking_slots')
        if not booking_slots:
            raise forms.ValidationError('This field is required.')
        return booking_slots


class MeetingForm(forms.ModelForm):
    meeting_title = forms.CharField(max_length=100)
    meeting_description = forms.Textarea
    meeting_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    meeting_slot = forms.ChoiceField(widget=forms.Select, required=True)

    class Meta:
        model = Meeting
        fields = ('meeting_title', 'meeting_description', 'meeting_date', 'meeting_slot')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MeetingForm, self).__init__(*args, **kwargs)
        adviser_slots = user.profile.adviser.profile.booking_slots  # get current adviser booking slots
        self.fields['meeting_slot'].choices = [(val, val) for val in adviser_slots]  # add them to the dropdown

    def clean_meeting_date(self):
        meeting_date = self.cleaned_data.get('meeting_date')
        if meeting_date < datetime.date.today():  # check if date is in the past
            raise forms.ValidationError("The date cannot be in the past!")
        return meeting_date

    def save(self, commit=True):
        meeting = super().save(commit=False)

        meeting.meeting_title = self.cleaned_data['meeting_title']
        meeting.meeting_description = self.cleaned_data['meeting_description']
        meeting.meeting_date = self.cleaned_data['meeting_date']
        meeting.meeting_slot = self.cleaned_data['meeting_slot']

        if commit:
            meeting.save()
        return meeting
