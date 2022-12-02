# Generated by Django 3.2.16 on 2022-12-02 01:15

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
            name='Pengguna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.TextField()),
                ('nomor_telepon', models.TextField(unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Konsumen_GOR',
            fields=[
                ('pengguna_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pengguna.pengguna')),
                ('status_loyalty', models.TextField()),
            ],
            bases=('pengguna.pengguna',),
        ),
        migrations.CreateModel(
            name='Pengurus_GOR',
            fields=[
                ('pengguna_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pengguna.pengguna')),
                ('akun_bank', models.TextField()),
            ],
            bases=('pengguna.pengguna',),
        ),
    ]
