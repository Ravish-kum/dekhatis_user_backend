# Generated by Django 4.2.2 on 2023-07-13 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_rename_checkout_view_serving_crm_table_cart_items_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serving_crm_table',
            name='cart_items_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
