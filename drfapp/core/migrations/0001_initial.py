# Generated by Django 2.2.6 on 2019-10-21 23:21

import django.db.models.deletion
from django.db import migrations, models

import drfapp.core.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('password',
                 models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True,
                                                    verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set',
                                                  related_query_name='user',
                                                  to='auth.Group',
                                                  verbose_name='groups')),
                ('organization', models.ForeignKey(blank=True, null=True,
                                                   on_delete=django.db.models.deletion.PROTECT,
                                                   related_name='users',
                                                   to='core.Organization')),
                ('user_permissions', models.ManyToManyField(blank=True,
                                                            help_text='Specific permissions for this user.',
                                                            related_name='user_set',
                                                            related_query_name='user',
                                                            to='auth.Permission',
                                                            verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', drfapp.core.models.UserManager()),
            ],
        ),
    ]
