# Generated by Django 3.1 on 2020-08-28 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200828_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealstoorder',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
