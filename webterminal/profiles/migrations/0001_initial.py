# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-05 05:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('send_contact_reminders', models.BooleanField(default=False)),
                ('send_birthday_reminders', models.BooleanField(default=False)),
                ('check_twitter_dms', models.BooleanField(default=True)),
                ('check_twitter_mentions', models.BooleanField(default=True)),
                ('check_foursquare', models.BooleanField(default=True)),
                ('phone_number', models.PositiveIntegerField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]