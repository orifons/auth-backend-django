from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError

from account.models import Profile


class CheckTokenPasswordAPIView(GenericAPIView):

    def get(self, request):
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            profile = get_object_or_404(Profile, id=uid)
            if not PasswordResetTokenGenerator().check_token(profile, token):
                return Response(
                    {'error': 'token is not valid, please check the new one'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            current_site = get_current_site(request).domain
            realtive_link = reverse('set-new-password', kwargs={'uidb64': uidb64})
            absolute_link = f'{request.scheme}://{current_site}{realtive_link}'

            return Response(
                {'success': True, 'message': 'Credential Valid', 'absolute_link': absolute_link},
                status=status.HTTP_200_OK
            )

        except DjangoUnicodeDecodeError as indentifier:
            print('Ocurred error', indentifier)
            return Response(
                {'error': 'token is not valid, please check the new one'},
                status=status.HTTP_401_UNAUTHORIZED
            )
