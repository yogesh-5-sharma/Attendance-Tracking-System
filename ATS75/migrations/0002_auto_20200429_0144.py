# Generated by Django 2.2.4 on 2020-04-28 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATS75', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='schedule_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='schedule_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
