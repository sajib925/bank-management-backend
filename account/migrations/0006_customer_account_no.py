# Generated by Django 5.0.6 on 2024-09-02 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_customer_account_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='account_no',
            field=models.CharField(blank=True, editable=False, max_length=12, null=True, unique=True),
        ),
    ]
