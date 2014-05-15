# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import rack.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('dosage_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('override_name', models.CharField(blank=True, max_length=100, null=True)),
                ('site_url', models.URLField(blank=True, null=True)),
                ('last_updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DosageUpdateReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('comic', models.ForeignKey(to_field='dosage_name', to='rack.Comic')),
                ('timestamp', models.DateTimeField(default=rack.models._utc_now)),
                ('status', models.IntegerField(choices=[(1, 'Success'), (2, 'Temporary Error'), (3, 'Error')])),
                ('stacktrace', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Strip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('comic', models.ForeignKey(to_field='dosage_name', to='rack.Comic')),
                ('url', models.URLField()),
                ('added_at', models.DateTimeField(default=rack.models._utc_now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
