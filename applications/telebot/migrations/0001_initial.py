# Generated by Django 4.0.4 on 2022-04-29 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeleSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200)),
                ('chat', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]
