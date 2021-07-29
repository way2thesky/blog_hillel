# Generated by Django 3.2.5 on 2021-07-29 10:16

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-publish']},
        ),
        migrations.AlterModelManagers(
            name='blog',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='blog',
            name='posted',
        ),
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
