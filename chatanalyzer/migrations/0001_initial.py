# Generated by Django 2.1.5 on 2019-03-23 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_id', models.IntegerField()),
                ('message_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('user_name', models.TextField()),
                ('user_last', models.TextField()),
                ('languaje_code', models.TextField()),
                ('chat_id', models.IntegerField()),
                ('chat_title', models.IntegerField()),
                ('type', models.TextField()),
                ('date', models.IntegerField()),
                ('text', models.TextField()),
            ],
        ),
    ]
