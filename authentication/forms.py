from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


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

    class Meta:
        model = Profile
        fields = ('user_type', 'school', 'study_year', 'booking_slots')

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

    def save(self, commit=True):
        profile = super().save(commit=False)

        profile.school = self.cleaned_data['school']
        profile.study_year = self.cleaned_data['study_year']

        if commit:
            profile.save()
        return profile
