# urls.py
from django.urls import path
from .views.login_views import LoginView, TestAuthenticationView
from .views.logout_views import LogoutUserView
from .views.forgot_pass_views import PasswordResetView, PasswordRestConfirm, SetNewPassword
from .views.userdetail_views import UserDetailView
from .views.userupdate_views import UserUpdateView
from .views.user_delete_views import UserDeleteView
# from .views.password_change_views import PasswordChangeView
from django.urls import path, re_path
from .views.views import SignupUserView
from .views.views import VerifyUserEmail

urlpatterns = [
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('test-auth/', TestAuthenticationView.as_view(), name='test-auth'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordRestConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('delete-account/', UserDeleteView.as_view(), name='delete-account'),
    path('user-update/', UserUpdateView.as_view(), name='user-update'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    # path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    # path('user-update-email/', UserUpdateEmailView.as_view(), name='user-update-email'),
    # other url patterns...
]
