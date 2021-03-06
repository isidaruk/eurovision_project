# Generated by Django 2.2.1 on 2019-05-30 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_auto_20190524_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='contests.Contest'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='countries.Country'),
        ),
    ]
