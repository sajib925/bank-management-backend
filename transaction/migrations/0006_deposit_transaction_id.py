# Generated by Django 5.1.2 on 2024-10-28 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_balancetransfer_deposit_loan_withdrawal'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]