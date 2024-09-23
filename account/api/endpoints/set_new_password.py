from smtplib import SMTPException

from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from account.models import Profile
from account.api.serializers import ResetPasswordSerializer


class SetNewPasswordAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ResetPasswordSerializer

    def patch(self, request):
        uidb64 = self.kwargs.get('uidb64')
        uid = smart_str(urlsafe_base64_decode(uidb64))
        profile = get_object_or_404(Profile, id=uid)

        serializer = self.serializer_class(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            profile.email_user(
                subject='Your password has been reset',
                message=f'The operation to reset your password has been successful.'
                        f' Thank you for continuing to use our site.',

            )

        except SMTPException:
            error = 'An error occured while sending email.'
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'success': 'Password is reset successfully'},
            status=status.HTTP_200_OK
        )
