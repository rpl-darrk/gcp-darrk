# Generated by Django 3.2.16 on 2022-12-03 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jadwal_Reservasi',
            fields=[
                ('ID_jadwal', models.AutoField(primary_key=True, serialize=False)),
                ('hari_buka', models.JSONField()),
                ('jam_buka', models.JSONField()),
                ('status_book', models.JSONField()),
            ],
        ),
    ]
