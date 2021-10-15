# Generated by Django 3.2.6 on 2021-10-15 15:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to='accounts/list', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'gif', 'svg'])]),
        ),
    ]