# Generated by Django 3.2.5 on 2021-07-26 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='short_description',
            field=models.CharField(max_length=250, unique_for_date='publish'),
        ),
    ]