# Generated by Django 2.2.6 on 2019-11-13 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitepaper',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='whitepaper',
            name='acceptor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='acceptor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='testquestions',
            name='id',
            field=models.UUIDField(default=uuid.UUID('426760d1-02e6-4191-8e67-5d7fbb19e199'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='videos',
            name='id',
            field=models.UUIDField(default=uuid.UUID('33ed7bce-03fa-4e50-b182-47a96dc240ed'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='whitepaper',
            name='uploader',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
    ]
