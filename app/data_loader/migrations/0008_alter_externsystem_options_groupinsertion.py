# Generated by Django 4.0.6 on 2022-08-01 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0007_alter_insertion_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='externsystem',
            options={'ordering': ['system_id']},
        ),
        migrations.CreateModel(
            name='GroupInsertion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('column_from', models.CharField(max_length=255)),
                ('column_to', models.CharField(max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_loader.filegroup')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_loader.table')),
            ],
        ),
    ]
