# Generated by Django 2.1.15 on 2022-05-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolios',
            fields=[
                ('agentID', models.IntegerField()),
                ('customerID', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
