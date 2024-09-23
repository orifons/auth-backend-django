from rest_framework import generics, permissions

from account.api.serializers import ChangeAvatarProfileSerializer


class ChangeAvatarAPIView(generics.UpdateAPIView):
    serializer_class = ChangeAvatarProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
