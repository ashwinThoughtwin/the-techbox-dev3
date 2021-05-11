# Generated by Django 3.1.7 on 2021-05-03 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_auto_20210422_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemassign',
            name='assign_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.item'),
        ),
        migrations.AlterField(
            model_name='itemassign',
            name='assign_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.employee'),
        ),
    ]
