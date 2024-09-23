from smtplib import SMTPException

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.generics import GenericAPIView, get_object_or_404

from account.models import Profile
from server_config.functions import send_email
from account.api.serializers import ResetPasswordEmailSerializer


class ResetPasswordEmailAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        profile = get_object_or_404(Profile, email=email)
        uidb64 = urlsafe_base64_encode(smart_bytes(profile.id))
        token = PasswordResetTokenGenerator().make_token(profile)

        current_site = get_current_site(request).domain
        realtivelink = reverse('check-token-password', kwargs={'uidb64': uidb64, 'token': token})

        absolute_uri = f'{request.scheme}://{current_site}{realtivelink}'
        subject = 'Reset your password'
        context = {'profile': profile, 'absolute_uri': absolute_uri}
        template_name = 'email/email_reset_password.html'

        try:
            send_email(template_name, context, subject, profile.email)

        except SMTPException:
            error = 'An error occured while sending email.'
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'successfully': 'check your email to reset your password.'}, status=status.HTTP_200_OK)
