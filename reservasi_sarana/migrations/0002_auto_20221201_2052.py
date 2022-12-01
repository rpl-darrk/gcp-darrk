# Generated by Django 3.2.16 on 2022-12-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservasi_sarana', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_pembayaran',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='detail_pembayaran',
            name='status',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pembatalan_sewa_sarana',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sewa_sarana',
            name='biaya',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sewa_sarana',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sewa_sarana',
            name='status',
            field=models.TextField(default='Menunggu pembayaran'),
        ),
        migrations.AlterField(
            model_name='verifikasi_pembatalan',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
