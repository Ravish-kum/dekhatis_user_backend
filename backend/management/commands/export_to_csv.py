import csv
import os
from django.core.management.base import BaseCommand
from backend.models import Query_table, Cancellations_table, Product, Shop_table, ThemeFurnituresBookings, ThemeFurniture, User, Customer_table,Advertisement_table,Review_table,Dekhatis_Delivery_table,Wood_Servicing_table,Query_CRM_table,Serving_CRM_table,User_CRM_table
#import pandas as pd

class Command(BaseCommand):
    help = 'Export data to CSV files'

    def handle(self, *args, **options):
        export_dir = '/home/ravish/dekhatis_database'

        # Create the export directory if it doesn't exist
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        models = [
            {'model': Query_table, 'Dekhatis_database': 'Query_table.csv', 'fields':['placing_id','customer_id','shop_id','item_id','item_cost','item_quantity','delivery_state', 'delivery_address','delivery_pin','delivery_phone','order_date','order_status','transaction_id','bank_id','shipping_otp','delivery_date','payment_status','dekhatis_payment_status','item_delivery_cost']},
            {'model': Cancellations_table, 'Dekhatis_database': 'cancellations_table.csv', 'fields': ['cancellation_id', 'placing_id','item_id', 'shop_id', 'customer_id', 'cancellations_date', 'order_date', 'order_status','transaction_id','bank_id']},
            {'model': Product, 'Dekhatis_database': 'Product.csv', 'fields': ['item_id', 'm_item_id', 'item_name', 'item_image', 'item_categories', 'item_detail', 'item_cost', 'item_revenue', 'shop_pin', 'item_date', 'shop_id', 'item_size', 'item_finish', 'item_storage', 'item_colour', 'item_room', 'item_shipping_time', 'item_visual_similarity', 'item_warrenty', 'item_instructions', 'item_rating', 'item_discount_percentage', 'item_availability','item_delivery_cost','item_recommended']},
            {'model': Shop_table, 'Dekhatis_database': 'Shop_table.csv', 'fields': ['id','shop_image','shop_id','shop_name','shop_brand_name','shop_email','shop_pass','shop_address','shop_phone','shop_alt','shop_pin','shop_date','manufacturer_name','manufacturer_address','manufacturer_phone','shop_service_availability','item_total_number','woodservicing_register']},
            {'model': ThemeFurnituresBookings, 'Dekhatis_database': 'ThemeFurnituresBookings.csv', 'fields': ['id', 'customer_id', 'shop_id','placing_id', 'theme_id', 'theme_order_status']},
            {'model': ThemeFurniture, 'Dekhatis_database': 'ThemeFurniture.csv', 'fields':['id', 'theme_cost', 'theme_date','theme_revenue', 'theme_availability', 'theme_discount_percentage', 'theme_image', 'details', 'theme_item_list']},
            {'model': User, 'Dekhatis_database': 'User.csv', 'fields': ['id', 'username', 'email', 'phone_number', 'is_phone_verified','otp','terms_conditions', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff']},
            {'model': Customer_table, 'Dekhatis_database': 'Customer_table.csv', 'fields': ['id','customer_id', 'customer_name', 'customer_email','customer_otp','customer_state', 'customer_address', 'customer_pin', 'customer_phone','customer_cerdits_tokens','customer_status']},
            {'model': Advertisement_table,'Dekhatis_database':'Advertisement_table.csv','fields':['adver_image','adver_url','paid_adver_date']},
            {'model': Review_table,'Dekhatis_database':'Review_table.csv','fields':['item_id','customer_id','comments','events']},
            {'model': Dekhatis_Delivery_table,'Dekhatis_database':'Dekhatis_Delivery_table.csv','fields':['id','delivery_merchant_id','order_id','delivery_payment','product_pickup_location','product_dropoff_location','item_id','delivery_merchant_payment']},
            {'model': Wood_Servicing_table,'Dekhatis_database':'Wood_Servicing_table.csv','fields':['servicing_placing_id','customer_id','shop_id','shop_pin','service_state','service_adderss','service_pin','service_phone','order_date','servicing_status','transaction_id','bank_id','service_date','payment_status','dekhatis_payment_status']},
            {'model': Query_CRM_table,'Dekhatis_database':'Query_CRM_table.csv','fields':['customer_id','customer_count','shop_id','shop_count','item_id','item_count','checkout_pincode','checkout_pincode_count','category','category_count','item_cost','item_cost_count','month','month_count','week','week_count','time','time_count','theme_id','theme_count']},
            {'model': Serving_CRM_table,'Dekhatis_database':'Serving_CRM_table.csv','fields':['searches','searches_count','category','category_count','price_item_view','price_item_view_count','cart_items','cart_items_count','checkout_view_count','description_view','description_view_count','theme_description_view','theme_description_view_count','theme_category','theme_category_count']},
            {'model': User_CRM_table, 'Dekhatis_database':'User_CRM_table.csv','fields':['age','age_count','gender','gender_count','income_level','income_level_count','pincode','pincode_count','individual_expenditure']}
            ]

        for model_info in models:
            model = model_info['model']
            filename = model_info['Dekhatis_database']
            fields = model_info['fields']

            # Get the data to export
            queryset = model.objects.all()
            file_path = os.path.join(export_dir, filename)

            '''
            # pandas implementations

            queryset_list = list(queryset.values())
            df = pd.DataFrame(queryset_list)
            pd.to_csv(filepath, df)
            self.stdout.write(self.style.SUCCESS(f'{model.__name__} data exported to {file_path}'))
            '''
            # Create the CSV file
            
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fields)
                for obj in queryset:
                    writer.writerow([getattr(obj, field) for field in fields])

            self.stdout.write(self.style.SUCCESS(f'{model.__name__} data exported to {file_path}'))
