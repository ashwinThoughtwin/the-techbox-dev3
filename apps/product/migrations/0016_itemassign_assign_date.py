# Generated by Django 3.1.7 on 2021-04-21 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20210421_0521'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemassign',
            name='assign_date',
            field=models.DateField(null=True),
        ),
    ]
