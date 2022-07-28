# Generated by Django 4.0.6 on 2022-07-28 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0005_auto_20220727_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='insertion',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='specialinsertion',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_loader.filegroup'),
        ),
    ]