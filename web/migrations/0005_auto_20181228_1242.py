# Generated by Django 2.1.4 on 2018-12-28 04:42

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20181228_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='icons'),
        ),
    ]