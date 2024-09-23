from rest_framework import generics, permissions

from account.api.serializers import ProfileUpdateSerializer


class ProfileUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
