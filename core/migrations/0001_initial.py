# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
        ('rack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('last_read', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, to='auth.Permission')),
                ('subscriptions', models.ManyToManyField(to='rack.Comic')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
