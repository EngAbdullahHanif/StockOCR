# Generated by Django 3.2 on 2021-05-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0008_itemtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='project_description',
            field=models.TextField(default='this is test'),
            preserve_default=False,
        ),
    ]
