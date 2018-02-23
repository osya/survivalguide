from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
# Create your models here.
from django.db.models import Count
from django.urls import reverse
from django.utils.text import slugify


class TalkListQuerySet(models.QuerySet):
    def list(self):
        return self.annotate(talk_count=Count('talks'))


class TalkList(models.Model):
    class Meta:
        unique_together = ('user', 'name')
        ordering = ('name', )

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='lists', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    objects = TalkListQuerySet.as_manager()

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(TalkList, self).save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse('talklists:detail', kwargs={'slug': self.slug})
