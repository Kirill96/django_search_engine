# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('text_of_url', models.TextField()),
                ('is_indexed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('rank', models.FloatField()),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Document')),
            ],
        ),
    ]
