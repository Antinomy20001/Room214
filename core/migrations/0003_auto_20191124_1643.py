# Generated by Django 2.2.7 on 2019-11-24 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191124_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='person',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Person'),
        ),
        migrations.AlterField(
            model_name='face',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
