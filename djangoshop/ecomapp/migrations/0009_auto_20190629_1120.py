# Generated by Django 2.2.2 on 2019-06-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0008_auto_20190629_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='ecomapp.Cart'),
        ),
    ]
