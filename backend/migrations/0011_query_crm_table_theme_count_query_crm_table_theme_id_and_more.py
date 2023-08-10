# Generated by Django 4.2.2 on 2023-08-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_alter_serving_crm_table_cart_items_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='query_crm_table',
            name='theme_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='query_crm_table',
            name='theme_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='serving_crm_table',
            name='theme_category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='serving_crm_table',
            name='theme_category_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='serving_crm_table',
            name='theme_description_view',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='serving_crm_table',
            name='theme_description_view_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_crm_table',
            name='individual_expenditure',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
