# Generated by Django 3.1 on 2020-09-04 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200904_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedmeals',
            name='mealstoorder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mealss', to='core.mealstoorder'),
        ),
    ]
