# Generated by Django 2.2.2 on 2019-07-02 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0016_auto_20190701_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(blank=True, to='ecomapp.CartItem'),
        ),
    ]
