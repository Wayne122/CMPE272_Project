# Generated by Django 2.2.7 on 2019-11-28 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0011_auto_20191127_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wpquiz',
            name='CA',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1),
        ),
    ]