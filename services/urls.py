from django.urls import path
from . import views
#from .views import signup, account_created


urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Signup URL
    path('submit_request/', views.submit_request, name='submit_request'),
    path('track_request/', views.track_request, name='track_request'),
    path('account_created/', views.account_created, name='account_created'),
]
