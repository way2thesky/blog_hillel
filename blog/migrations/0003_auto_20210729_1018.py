# Generated by Django 3.2.5 on 2021-07-29 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210729_1016'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='blog',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='blog',
            name='status',
        ),
        migrations.AddField(
            model_name='blog',
            name='posted',
            field=models.BooleanField(default=False),
        ),
    ]