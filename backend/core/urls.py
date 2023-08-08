from django.urls import path

from . import views

urlpatterns = [
    path('getcode/', views.get_code, name='Get code'),
    path('checkcode/', views.check_code, name='Check code'),
    path('getprofile/', views.get_profile, name='Get profile'),
    path('enterinvite/', views.enter_invite, name='Enter invite code'),
    path('refresh/', views.refresh_tokens, name='Refresh tokens'),
]