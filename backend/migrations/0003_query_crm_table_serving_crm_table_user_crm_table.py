# Generated by Django 4.2.2 on 2023-07-09 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_customer_table_customer_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query_CRM_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(blank=True, max_length=20, null=True)),
                ('customer_count', models.ImageField(blank=True, null=True, upload_to='')),
                ('shop_id', models.CharField(blank=True, max_length=20, null=True)),
                ('shop_count', models.IntegerField(blank=True, null=True)),
                ('item_id', models.CharField(blank=True, max_length=20, null=True)),
                ('item_count', models.IntegerField(blank=True, null=True)),
                ('checkout_pincode', models.IntegerField(blank=True, null=True)),
                ('checkout_pincode_count', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('category_count', models.IntegerField(blank=True, null=True)),
                ('item_cost', models.IntegerField(blank=True, null=True)),
                ('item_cost_count', models.IntegerField(blank=True, null=True)),
                ('month', models.CharField(blank=True, max_length=50, null=True)),
                ('month_count', models.IntegerField(blank=True, null=True)),
                ('week', models.CharField(blank=True, max_length=20, null=True)),
                ('week_count', models.IntegerField(blank=True, null=True)),
                ('time', models.CharField(blank=True, max_length=50, null=True)),
                ('time_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'query_CRM_table',
            },
        ),
        migrations.CreateModel(
            name='Serving_CRM_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('searches', models.CharField(blank=True, max_length=20, null=True)),
                ('searches_count', models.IntegerField(blank=True, null=True)),
                ('category_cost', models.IntegerField(blank=True, null=True)),
                ('category_count', models.IntegerField(blank=True, null=True)),
                ('price_item_view', models.CharField(blank=True, max_length=50, null=True)),
                ('price_item_view_count', models.IntegerField(blank=True, null=True)),
                ('colour_item_view', models.CharField(blank=True, max_length=20, null=True)),
                ('colour_item_view_count', models.IntegerField(blank=True, null=True)),
                ('description_view', models.CharField(blank=True, max_length=50, null=True)),
                ('description_view_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'serving_CRM_table',
            },
        ),
        migrations.CreateModel(
            name='User_CRM_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(blank=True, max_length=20, null=True)),
                ('age_count', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('gender_count', models.IntegerField(blank=True, null=True)),
                ('income_level', models.CharField(blank=True, max_length=50, null=True)),
                ('income_level_count', models.IntegerField(blank=True, null=True)),
                ('pincode', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_CRM_table',
            },
        ),
    ]
