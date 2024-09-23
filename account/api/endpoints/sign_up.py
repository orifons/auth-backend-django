import jwt
from smtplib import SMTPException
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site

from server_config import settings
from account.models import Profile
from server_config.functions import send_email
from account.api.serializers import RegisterProfileSerializer


class SignUpAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegisterProfileSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        profile = get_object_or_404(Profile, email=serializer.data['email'])
        token = RefreshToken.for_user(profile).access_token

        current_site = get_current_site(request).domain
        realtive_link = reverse('verify-account', kwargs={'token': token})
        absolute_uri = f'{request.scheme}://{current_site}{realtive_link}'

        context = {'profile': profile, 'absolute_uri': absolute_uri}
        template_name = 'email/email_register.html'

        subject = 'Activate your account'

        try:
            send_email(template_name, context, subject, profile.email)

        except SMTPException:
            profile.delete()
            return Response({'error': f'An error occured while sending email.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'check your email to activate your account.'}, status=status.HTTP_201_CREATED)


class VerifyAccountAPIView(GenericAPIView):
    def get(self, request):
        token = self.kwargs.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            profile = get_object_or_404(Profile, id=payload['user_id'])

            if not profile.is_active:
                profile.is_active = True
                profile.save()
                profile.email_user(
                    subject='Your account has been verified',
                    message=(
                        f'Hi {profile.get_full_name()}, Your account has been verified \n \n'
                        f'Thanks for register'
                    ),
                    from_email=None,
                )
                return Response({'success': 'Successfully activated.'}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Account already activated.'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
