# Generated by Django 3.2.6 on 2022-08-21 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(upload_to='posts/%Y/%m/%d'),
        ),
    ]
