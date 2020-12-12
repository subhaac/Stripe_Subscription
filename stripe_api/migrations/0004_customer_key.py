# Generated by Django 3.1.4 on 2020-12-12 14:55

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0003_auto_20201207_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='key',
            field=fernet_fields.fields.EncryptedTextField(default='null'),
            preserve_default=False,
        ),
    ]