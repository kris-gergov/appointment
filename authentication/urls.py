from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('change_slots/', views.change_slots, name="change_slots"),
    path('meeting/', views.meeting, name="meeting"),
    path('meeting/', views.meeting, name="meeting"),
    path('meeting/<int:pk>', views.meeting_detail_, name='meeting_detail'),
    path('unconfirmed_meetings/', views.unconfirmed_meeting_list, name="unconfirmed_meetings"),
    path('confirmed_meetings/', views.confirmed_meeting_list, name="confirmed_meetings"),
    path('past_meetings/', views.past_meeting_list, name="past_meetings"),
    path('confirm_specific_meeting/<int:pk>/', views.confirm_specific_meeting, name="confirm_specific_meeting"),
    path('unconfirm_specific_meeting/<int:pk>/', views.unconfirm_specific_meeting, name="unconfirm_specific_meeting"),
    path('cancel_specific_meeting/<int:pk>/', views.cancel_specific_meeting, name="cancel_specific_meeting"),
]
