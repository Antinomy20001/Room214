# Generated by Django 2.2.7 on 2019-11-25 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191124_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='student_id',
            field=models.TextField(null=True),
        ),
    ]
