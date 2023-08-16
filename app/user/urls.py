"""
URL mappings for the user API.
"""
from django.urls import path
from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# used for reverse mapping defined in test_user_api.py:
# CREATE_USER_URL = reverse('user:create')
app_name = 'user'

# Any request that is pssed through url
# will be handled by the CreateUserView (or others defined) inside views.py
# name='create' is also used for reverse lookup in test_user_api.py:
# CREATE_USER_URL = reverse('user:create')
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', views.index, name='index'),
    path('login/', views.LoginUserView.login_view, name='login'),
    path('profile/', views.getUserProfile, name='profile'),
    path('profiles-list/', views.getUsersList, name='profiles-list'),
    path('register/', views.registerUser, name='register'),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
