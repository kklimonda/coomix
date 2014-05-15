# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('strip', models.ForeignKey(to_field='id', to='rack.Strip')),
                ('order', models.IntegerField()),
                ('image', models.ImageField(upload_to='strips/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
