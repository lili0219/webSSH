# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-10 12:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wssh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatedatetime', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='Update time')),
                ('createdatetime', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('groups', models.ManyToManyField(to='wssh.ServerGroup', verbose_name='Server Group')),
                ('permissions', models.ManyToManyField(related_name='permission', to='auth.Permission', verbose_name='Permission')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='permissionuser', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'permissions': (('can_add_user', 'Can add user'), ('can_change_user', 'Can change user info'), ('can_delete_user', 'Can delete user info'), ('can_view_user', 'Can view user info'), ('can_view_permissions', 'Can view user permissions'), ('can_change_permissions', 'Can change user permissions'), ('can_delete_permissions', 'Can revoke user permissions'), ('can_add_permissions', 'Can add user permissions')),
            },
        ),
    ]
