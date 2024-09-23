from rest_framework import serializers

from account.models import Profile


class RegisterProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Profile
        fields = (
            'username', 'email', 'first_name', 'last_name', 'phone_number', 'address',
            'city', 'country', 'avatar', 'password', 'password_confirm'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        username = self.validated_data['username']
        email = self.validated_data['email']
        phone_number = self.validated_data['phone_number']
        password = self.validated_data['password']
        password2 = self.validated_data['password_confirm']

        if Profile.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'This user already exists'})

        if Profile.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'This email already exists'})

        if Profile.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({'error': 'This phone number already exists'})

        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords must match'})

        profile = Profile.objects.create_user(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=username,
            email=email,
            password=password,
            is_active=False,
        )

        profile.phone_number = phone_number
        profile.address = self.validated_data['address']
        profile.city = self.validated_data['city']
        profile.country = self.validated_data['country']
        profile.avatar = self.validated_data['avatar']
        profile.set_password = password
        profile.save()

        return profile
