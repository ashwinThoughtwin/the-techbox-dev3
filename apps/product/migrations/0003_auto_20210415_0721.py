# Generated by Django 3.1.7 on 2021-04-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210415_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.CharField(choices=[('1', 'Team Lead'), ('2', 'Sr. Developer'), ('3', 'Jr. Developer')], max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mobile',
            field=models.CharField(max_length=12),
        ),
    ]
