# Generated by Django 2.2.1 on 2019-05-30 13:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0002_auto_20190529_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='point',
            field=models.PositiveIntegerField(choices=[(1, '1 Point'), (2, '2 Points'), (3, '3 Points'), (4, '4 Points'), (5, '5 Points'), (6, '6 Points'), (7, '7 Points'), (8, '8 Points'), (10, '10 Point'), (12, '12 Points')], default=1, validators=[django.core.validators.MaxValueValidator(12)]),
        ),
    ]
