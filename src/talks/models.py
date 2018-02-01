from django.conf.global_settings import AUTH_USER_MODEL
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.utils.text import slugify


class TalkListQuerySet(models.QuerySet):
    def list(self):
        return self.annotate(talk_count=Count('talks'))


class TalkList(models.Model):
    class Meta:
        unique_together = ('user', 'name')
        ordering = ('name',)

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='lists')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    objects = TalkListQuerySet.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(TalkList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('talks:talk_lists:detail', kwargs={'slug': self.slug})


class Talk(models.Model):
    class Meta:
        ordering = ('when', 'room')
        unique_together = ('talk_list', 'name')

    ROOM_CHOICES = (
        ('517D', '517D'),
        ('517C', '517C'),
        ('517AB', '517AB'),
    )
    talk_list = models.ForeignKey(TalkList, related_name='talks')
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='talks')
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    when = models.DateTimeField(null=True)
    room = models.CharField(max_length=5, choices=ROOM_CHOICES, blank=True)
    host = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Talk, self).save(*args, **kwargs)
