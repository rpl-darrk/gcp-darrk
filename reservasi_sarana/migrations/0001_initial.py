# Generated by Django 3.2.16 on 2022-12-10 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pengguna', '0001_initial'),
        ('sarana_olahraga', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pembatalan_Sewa_Sarana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('pembatal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pengguna.pengguna')),
            ],
        ),
        migrations.CreateModel(
            name='Status_Detail_Pembayaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Belum upload bukti pembayaran'), (1, 'Menunggu verifikasi bukti pembayaran'), (2, 'Pembayaran terverifikasi')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Status_Sewa_Sarana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Menunggu pembayaran'), (1, 'Berhasil dibayar'), (2, 'Batal'), (3, 'Selesai')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Status_Verifikasi_Pembatalan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Pembatalan diajukan'), (1, 'Pembatalan terverifikasi')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Verifikasi_Pembatalan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.TextField(default=0)),
                ('pembatalan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservasi_sarana.pembatalan_sewa_sarana')),
                ('pengurus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pengguna.pengurus_gor')),
            ],
        ),
        migrations.CreateModel(
            name='Sewa_Sarana',
            fields=[
                ('ID_sewa', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('biaya', models.FloatField(default=0)),
                ('status', models.TextField(default=0)),
                ('jam_booking', models.JSONField()),
                ('konsumen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pengguna.konsumen_gor')),
                ('pengurus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pengguna.pengurus_gor')),
                ('sarana', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sarana_olahraga.sarana')),
            ],
        ),
        migrations.AddField(
            model_name='pembatalan_sewa_sarana',
            name='sewa_sarana',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservasi_sarana.sewa_sarana'),
        ),
        migrations.CreateModel(
            name='Detail_Pembayaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.TextField(default=0)),
                ('bukti_pembayaran', models.TextField(blank=True, null=True)),
                ('sewa_sarana', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservasi_sarana.sewa_sarana')),
            ],
        ),
    ]
