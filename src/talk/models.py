# noinspection PyPackageRequirements
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

from autoslug import AutoSlugField

from talklist.models import TalkList


class Talk(models.Model):
    class Meta:
        ordering = ('when', 'room')
        unique_together = ('talklist', 'name')

    ROOM_CHOICES = (
        ('517D', '517D'),
        ('517C', '517C'),
        ('517AB', '517AB'),
    )
    talklist = models.ForeignKey(TalkList, related_name='talks', on_delete=models.PROTECT)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='talks', on_delete=models.PROTECT)
    name = models.CharField(max_length=255, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    when = models.DateTimeField(null=True)
    room = models.CharField(max_length=5, choices=ROOM_CHOICES, blank=True)
    host = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
