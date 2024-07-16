# urls.py
from django.urls import path
from .views.login_views import LoginView
from .views.logout_views import logout_view
from .views.forgot_pass_views import PasswordResetView
from .views.signup_views import SignupSerializer
from .views.otp_views import OTPVerificationView
from .views.userdetail_views import UserDetailView
from .views.userupdate_views import UserUpdateView
from .views.user_delete_views import UserDeleteView
from .views.password_change_views import PasswordChangeView
from .views.user_update_email_views import UserUpdateEmailView
from django.urls import path, re_path

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', PasswordResetView.as_view(), name='forgot-password'),
    path('signup/', SignupSerializer, name='signup'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('user-update/', UserUpdateView.as_view(), name='user-update'),
    path('user-delete/', UserDeleteView.as_view(), name='user-delete'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('user-update-email/', UserUpdateEmailView.as_view(), name='user-update-email'),
    # other url patterns...
]
