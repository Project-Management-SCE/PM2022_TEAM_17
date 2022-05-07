# Generated by Django 2.1.15 on 2022-05-07 11:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(default='user', max_length=300, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must be alphanumeric or contain numbers', regex='^[a-zA-Z0-9.+-]*$')])),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_Customer', models.BooleanField(default=False)),
                ('is_Agent', models.BooleanField(default=False)),
                ('is_Admin', models.BooleanField(default=False)),
                ('full_name', models.CharField(max_length=80)),
                ('city', models.CharField(max_length=50)),
                ('Mobile', models.CharField(max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('isConfirmedAgent', models.BooleanField(default=False)),
                ('isPortfolio', models.CharField(choices=[('waiting', 'waiting'), ('confirmed', 'confirmed'), ('declined', 'declined'), ('None', 'None')], default='None', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
