import os
import shutil

from django.db import models
from django.dispatch import receiver

from account.models import Profile


def _delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


@receiver(models.signals.post_delete, sender=Profile)
def delete_file(sender, instance: Profile, *args, **kwargs):
    if instance.avatar:
        _delete_file(instance.avatar.path)
