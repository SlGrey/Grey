# Generated by Django 2.2.2 on 2019-07-02 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0021_auto_20190702_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Cart'),
            preserve_default=False,
        ),
    ]
