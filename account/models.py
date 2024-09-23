import os
from functools import partial

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator

from server_config.functions import file_directory_path


class Profile(AbstractUser):
    phone_number = models.CharField(
        max_length=11, unique=True, validators=[
            RegexValidator(
                regex=r'^\+53\d{8,10}$',
                message="El número de teléfono debe estar en el formato: '+53-XXXXXXXX'."
            )
        ]
    )

    address = models.CharField(max_length=120)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=60)

    avatar = models.ImageField(upload_to=partial(file_directory_path, data=["username"]), blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'email', 'first_name', 'last_name', 'phone_number'
    ]

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['date_joined']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self.pk:
            old_avatar = Profile.objects.get(pk=self.pk).avatar

            if old_avatar and old_avatar != self.avatar:
                path_avatar = old_avatar.path

                if os.path.isfile(path_avatar):
                    os.remove(path_avatar)

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.avatar:
            self.avatar.delete()
        super(Profile, self).delete()
