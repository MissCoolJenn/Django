# Generated by Django 4.0 on 2023-02-12 17:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pub_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date time field'),
            preserve_default=False,
        ),
    ]
