# Generated by Django 2.2.1 on 2019-07-05 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0003_auto_20190522_1558'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={},
        ),
        migrations.AlterField(
            model_name='contest',
            name='host_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contests', to='countries.Country'),
        ),
    ]
