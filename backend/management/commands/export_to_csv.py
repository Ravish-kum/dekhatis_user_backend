import csv
import os
from django.core.management.base import BaseCommand
from backend.models import Query_table, Cancellations_table, Product, Shop_table, ThemeFurnituresBookings, ThemeFurniture, User, Customer_table

class Command(BaseCommand):
    help = 'Export data to CSV files'

    def handle(self, *args, **options):
        export_dir = '/home/ravish/dekhatis_database'

        # Create the export directory if it doesn't exist
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        models = [
            {'model': Query_table, 'Dekhatis_database': 'Query_table.csv', 'fields':['placing_id','customer_id','shop_id','item_id','item_cost','item_quantity','delivery_state', 'delivery_address','delivery_pin','delivery_phone','order_date','order_status','transaction_id','bank_id']},
            {'model': Cancellations_table, 'Dekhatis_database': 'cancellations_table.csv', 'fields': ['cancellation_id', 'placing_id', 'shop_id', 'customer_id', 'cancellations_date', 'order_date', 'order_status','transaction_id','bank_id']},
            {'model': Product, 'Dekhatis_database': 'Product.csv', 'fields': ['item_id', 'm_item_id', 'item_name', 'item_image', 'item_categories', 'item_detail', 'item_cost', 'item_revenue', 'shop_pin', 'shop_id', 'item_size', 'item_finish', 'item_storage', 'item_colour', 'item_room', 'item_shipping_time', 'item_visual_similarity', 'item_warrenty', 'item_instructions', 'item_rating', 'item_discount_percentage', 'item_availability']},
            {'model': Shop_table, 'Dekhatis_database': 'Shop_table.csv', 'fields': ['id','shop_id','shop_name','shop_brand_name','shop_email','shop_pass','shop_address','shop_phone','shop_alt','shop_pin','shop_date','manufacturer_name','manufacturer_address','manufacturer_phone','shop_ordered']},
            {'model': ThemeFurnituresBookings, 'Dekhatis_database': 'ThemeFurnituresBookings.csv', 'fields': ['id', 'customer_id', 'shop_id','placing_id', 'theme_id', 'theme_order_status']},
            {'model': ThemeFurniture, 'Dekhatis_database': 'ThemeFurniture.csv', 'fields':['id', 'theme_cost', 'theme_date','theme_revenue', 'theme_availability', 'theme_discount_percentage', 'theme_image', 'details', 'theme_item_list']},
            {'model': User, 'Dekhatis_database': 'User.csv', 'fields': ['id', 'username', 'email', 'phone_number', 'is_phone_verified','otp','terms_conditions', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff']},
            {'model': Customer_table, 'Dekhatis_database': 'Customer_table.csv', 'fields': ['id','customer_id', 'customer_name', 'customer_email','customer_otp','customer_state', 'customer_address', 'customer_pin', 'customer_phone','customer_cerdits_tokens']},
        ]

        for model_info in models:
            model = model_info['model']
            filename = model_info['Dekhatis_database']
            fields = model_info['fields']

            # Get the data to export
            queryset = model.objects.all()

            # Create the CSV file
            file_path = os.path.join(export_dir, filename)
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fields)
                for obj in queryset:
                    writer.writerow([getattr(obj, field) for field in fields])

            self.stdout.write(self.style.SUCCESS(f'{model.__name__} data exported to {file_path}'))
