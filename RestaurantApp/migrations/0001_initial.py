# Generated by Django 4.1 on 2023-05-28 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
