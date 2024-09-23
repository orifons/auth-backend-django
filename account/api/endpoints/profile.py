from rest_framework import generics, permissions

from account.api.permissions import IsOwner
from account.api.serializers import ProfileSerializer


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwner]

    def get_object(self):
        return self.request.user
