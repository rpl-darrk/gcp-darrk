# Generated by Django 3.2.16 on 2022-12-10 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pengguna', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GOR',
            fields=[
                ('ID_gor', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=200)),
                ('url_foto', models.CharField(max_length=200)),
                ('alamat', models.CharField(max_length=200)),
                ('nomor_telepon', models.CharField(max_length=200)),
                ('pengurus', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pengguna.pengurus_gor')),
            ],
        ),
        migrations.CreateModel(
            name='Jadwal_Reservasi',
            fields=[
                ('ID_jadwal', models.AutoField(primary_key=True, serialize=False)),
                ('hari_buka', models.JSONField(null=True)),
                ('jam_buka', models.JSONField(null=True)),
                ('status_book', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sarana',
            fields=[
                ('ID_sarana', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=200)),
                ('url_foto', models.CharField(max_length=200)),
                ('jenis', models.CharField(choices=[('Lapangan Basket', 'Lapangan Basket'), ('Lapangan Bulutangkis', 'Lapangan Bulu Tangkis'), ('Lapangan Futsal', 'Lapangan Futsal'), ('Kolam Renang', 'Kolam Renang'), ('Lapangan Sepak Bola', 'Lapangan Sepak Bola')], max_length=200)),
                ('deskripsi', models.TextField()),
                ('gor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sarana_olahraga.gor')),
                ('id_jadwal_reservasi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sarana_olahraga.jadwal_reservasi')),
            ],
        ),
    ]
