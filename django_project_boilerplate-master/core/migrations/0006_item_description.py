# Generated by Django 3.0 on 2019-12-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='This is the test discription sdfdsdf sd fs df sdf  fdsdsfdsf'),
            preserve_default=False,
        ),
    ]
