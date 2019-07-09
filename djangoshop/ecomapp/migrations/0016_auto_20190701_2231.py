# Generated by Django 2.2.2 on 2019-07-01 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0015_auto_20190701_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='ecomapp.CartItem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
    ]