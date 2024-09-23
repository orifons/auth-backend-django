from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from account.models import Profile
from account.api.serializers import MyTokenObtainPairSerializer, ProfileSerializer


class SignInAPIView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, args, kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = Profile.objects.get(id=response.data['user']['id'])
            response.data.update({'user': ProfileSerializer(user, context={'request': request}).data})
            return response
        return response
