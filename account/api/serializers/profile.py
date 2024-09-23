from rest_framework import serializers

from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['password']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = [
            'password', 'avatar', 'is_active', 'is_staff', 'is_superuser',
            'date_joined', 'last_login', 'user_permissions', 'groups'
        ]


class ChangeAvatarProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Profile
        fields = [
            'old_password', 'new_password', 'confirm_password'
        ]

    def save(self):
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']
        confirm_password = self.validated_data['confirm_password']

        profile: Profile = self.instance

        if not profile.check_password(old_password):
            raise serializers.ValidationError({'error': 'The current password is invalid.'})

        if new_password != confirm_password:
            raise serializers.ValidationError({'error': 'Passwords must match'})

        profile.set_password(new_password)
        profile.save()

        return profile
