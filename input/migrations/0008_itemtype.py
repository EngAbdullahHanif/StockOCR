# Generated by Django 3.2 on 2021-05-06 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0007_project_item_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
