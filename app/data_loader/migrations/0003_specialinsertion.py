# Generated by Django 4.0.6 on 2022-07-25 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0002_rename_sustitution_insertion'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialInsertion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_to', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_loader.file')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_loader.table')),
            ],
        ),
    ]
