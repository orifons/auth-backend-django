from django.urls import path

from account.api.endpoints import ProfileAPIView, ProfileUpdateDeleteAPIView, SignInAPIView, \
    SignUpAPIView, ChangeAvatarAPIView, ChangePasswordAPIView, VerifyAccountAPIView, \
    ResetPasswordEmailAPIView, CheckTokenPasswordAPIView, SetNewPasswordAPIView

urlpatterns = [
    path('account/token/', SignInAPIView.as_view(), name='sign-in'),
    path('account/sign_up/', SignUpAPIView.as_view(), name='sign-up'),
    path('account/verify-account/<token>/', VerifyAccountAPIView.as_view(), name="verify-account"),
    path('account/me/', ProfileAPIView.as_view(), name='profile'),
    path('account/me/update/', ProfileUpdateDeleteAPIView.as_view(), name='profile-update'),
    path('account/me/change_avatar/', ChangeAvatarAPIView.as_view(), name='change-avatar'),
    path('account/me/change_password/', ChangePasswordAPIView.as_view(), name='change-password'),

    path('account/reset-password-email/', ResetPasswordEmailAPIView.as_view(), name='reset-password-email'),
    path('account/check-token-password/<uidb64>/<token>/', CheckTokenPasswordAPIView.as_view(), name='check-token-password'),
    path('account/set-new-password/<uidb64>/', SetNewPasswordAPIView.as_view(), name='set-new-password')
]
