# Generated by Django 4.2.2 on 2023-07-13 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_remove_serving_crm_table_category_cost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serving_crm_table',
            old_name='colour_item_view',
            new_name='checkout_view',
        ),
        migrations.RenameField(
            model_name='serving_crm_table',
            old_name='colour_item_view_count',
            new_name='checkout_view_count',
        ),
    ]
