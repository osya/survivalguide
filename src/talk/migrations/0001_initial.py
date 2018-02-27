# pylint: disable=C0103
# Generated by Django 2.0.2 on 2018-02-21 16:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('talklist', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255)),
                ('when', models.DateTimeField(null=True)),
                ('room',
                 models.CharField(
                     blank=True, choices=[('517D', '517D'), ('517C', '517C'), ('517AB', '517AB')], max_length=5)),
                ('host', models.CharField(blank=True, max_length=255)),
                ('talklist',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.PROTECT, related_name='talks', to='talklist.TalkList')),
                ('user',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.PROTECT, related_name='talks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('when', 'room'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='talk',
            unique_together={('talklist', 'name')},
        ),
    ]
