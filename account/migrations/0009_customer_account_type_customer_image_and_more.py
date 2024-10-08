# Generated by Django 5.1.1 on 2024-09-21 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_customer_account_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='account_type',
            field=models.CharField(blank=True, choices=[('SAVINGS', 'Savings Account'), ('CHECKING', 'Checking Account'), ('BUSINESS', 'Business Account'), ('JOINT', 'Joint Account'), ('CURRENT', 'Current Account')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='religion',
            field=models.CharField(blank=True, choices=[('ISLAM', 'Islam'), ('CHRISTIANITY', 'Christianity'), ('HINDUISM', 'Hinduism'), ('BUDDHISM', 'Buddhism'), ('JUDAISM', 'Judaism'), ('ATHEISM', 'Atheism'), ('OTHER', 'Other')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='manager',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='manager',
            name='religion',
            field=models.CharField(blank=True, choices=[('ISLAM', 'Islam'), ('CHRISTIANITY', 'Christianity'), ('HINDUISM', 'Hinduism'), ('BUDDHISM', 'Buddhism'), ('JUDAISM', 'Judaism'), ('ATHEISM', 'Atheism'), ('OTHER', 'Other')], max_length=30, null=True),
        ),
    ]
