from rest_framework import generics, permissions, status
from rest_framework.response import Response

from account.api.serializers import ChangePasswordSerializer


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)
        return Response(
            {'success': 'Your password has been changed successfully'},
            status=status.HTTP_200_OK
        )
