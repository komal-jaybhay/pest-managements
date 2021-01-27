from django.db import models
import django
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Insect(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, default=None, blank=True)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    creation_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class InsectAdvisory(models.Model):
    insect_name = models.OneToOneField(Insect, on_delete=models.CASCADE)
    advisory = models.TextField(default=None)
    suggestion = models.TextField(default=None)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    creation_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # creation_by = models.CharField(max_length=256)