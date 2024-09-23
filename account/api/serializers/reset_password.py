from rest_framework import serializers

from account.models import Profile


class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Profile
        fields = ['new_password', 'confirm_password']

    def save(self, **kwargs):
        new_password = self.validated_data['new_password']
        confirm_password = self.validated_data['confirm_password']

        profile: Profile = self.instance

        if new_password != confirm_password:
            raise serializers.ValidationError({'error': 'Passwords must match'})

        profile.set_password(new_password)
        profile.save()

        return profile
