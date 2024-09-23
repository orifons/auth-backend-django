from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.api.serializers import ProfileSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        return validated_data

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = ProfileSerializer(self.user).data
        return data
