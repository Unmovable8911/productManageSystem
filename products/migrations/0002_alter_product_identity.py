# Generated by Django 5.0.2 on 2024-02-22 12:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='identity',
            field=models.UUIDField(db_comment='primary_key', default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]