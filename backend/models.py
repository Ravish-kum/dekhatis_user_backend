from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
import datetime
import uuid
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.db import models
from django.contrib import admin
import os
from twilio.rest import Client
import random
# Create your models here.

class Product(models.Model):
    item_id = models.CharField(max_length=30,primary_key = True )
    m_item_id = models.CharField(max_length=30, blank=True)
    item_name = models.CharField(max_length=50)
    item_image = models.ImageField(upload_to='uploads/images',blank=True)
    item_categories = models.CharField(max_length=30)
    item_detail= models.CharField(max_length=300)
    item_cost = models.IntegerField()
    item_revenue = models.IntegerField()
    shop_pin= models.IntegerField()
    item_date=models.DateTimeField(auto_now_add=True,null=True, blank=True)
    shop_id= models.ForeignKey("Shop_table", verbose_name= "placer",default=1, on_delete=models.CASCADE)
    item_size = models.CharField(max_length=30,blank=True)
    item_finish = models.CharField(max_length=30,blank=True)
    item_storage = models.CharField(max_length=30,blank=True)
    item_colour = models.CharField(max_length=30,blank=True)
    item_room = models.CharField(max_length=20,blank=True)
    item_shipping_time = models.CharField(max_length=30)
    item_visual_similarity= models.CharField(max_length=30,blank=True)
    item_warrenty = models.CharField(max_length=30,blank=True)
    item_instructions = models.CharField(max_length=30,blank=True)
    item_rating = models.IntegerField(default=0)
    item_discount_percentage = models.CharField(max_length=100, null=True, blank=True) 
    item_availability = models.CharField(max_length=100,blank=True, null=True)
    item_delivery_cost = models.DecimalField(null = True ,blank=True, max_digits=10, decimal_places=2) 
    item_recommended = models.CharField(max_length=100,blank=True, null=True     )
    class Meta:
        db_table='product'

class Shop_table(models.Model):
    id = models.AutoField(primary_key=True)
    shop_image = models.ImageField(upload_to='uploads/images',blank=True)
    shop_id= models.CharField(max_length=30,unique = True )
    shop_name= models.CharField(max_length=45)
    shop_brand_name= models.CharField(max_length=45,blank=True)
    shop_email= models.EmailField()
    shop_pass= models.CharField(max_length=200,blank=True)
    shop_address= models.CharField(max_length=300)
    shop_phone= models.CharField(max_length=14)
    shop_alt= models.CharField(max_length=14)
    shop_pin= models.IntegerField()
    shop_date=models.DateTimeField(auto_now_add=True,null=True, blank=True)
    manufacturer_name= models.CharField(max_length=45)
    manufacturer_address =models.CharField(max_length=45)
    manufacturer_phone =models.IntegerField(default=0)
    shop_service_availability= models.CharField(max_length=50,blank=True)
    item_total_number = models.IntegerField(blank=True, null =True)
    woodservicing_register = models.CharField(max_length=50,blank=True, null =True)

    def check_password(self, raw_password):
        
        hasher = PBKDF2PasswordHasher()
        merchant_match= hasher.verify(raw_password, self.shop_pass)
        print(merchant_match)
        return merchant_match
    class Meta:
        db_table='shop_table'

class Customer_table(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id= models.CharField(max_length = 100,blank=True,unique=True)
    customer_name= models.CharField(max_length=45)
    customer_email= models.EmailField()
    customer_otp= models.CharField(max_length=20,blank=True)
    customer_state= models.CharField(max_length=200,blank=True)
    customer_address= models.CharField(max_length=300,blank=True)
    customer_pin =models.IntegerField(default=0)
    customer_phone= models.CharField(max_length=14,blank=True)
    customer_cerdits_tokens= models.IntegerField(default= 0)
    customer_status= models.CharField(max_length=50,blank=True,null=True)
    class Meta:
        db_table='customer_table'

    
class Query_table(models.Model):
    placing_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    customer_id= models.ForeignKey("Customer_table", verbose_name= "user",default=1, on_delete=models.SET_DEFAULT)
    shop_id = models.ForeignKey("Shop_table", verbose_name= "shop", default=1,on_delete=models.SET_DEFAULT)
    item_id = models.ForeignKey("Product", verbose_name= "item",default=1, on_delete=models.SET_DEFAULT)
    item_cost = models.IntegerField()
    item_quantity =models.IntegerField(default=1)
    delivery_state= models.CharField(max_length=200,blank=True)
    delivery_address= models.CharField(max_length=300,blank=True)
    delivery_pin =models.IntegerField(default=0)
    delivery_phone= models.CharField(max_length=14,blank=True)
    order_date= models.DateTimeField(auto_now_add=True,null=True, blank=True)
    order_status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=200)
    bank_id=models.CharField(max_length=200,blank=True)
    shipping_otp= models.IntegerField(null=True,blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    payment_status =models.CharField(max_length=200,null=True,blank=True)
    dekhatis_payment_status = models.CharField(max_length=200,null=True,blank=True)
    item_delivery_cost=models.DecimalField(null = True ,blank=True, max_digits=10, decimal_places=2)
    
    def custom_save(self, *args, **kwargs):
        print('customesave')
        return super().save(*args, **kwargs)


    def save(self, *args, **kwargs):
        print('normalsave')
        
        """
            try:
                account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
                print(self.customer_id.customer_name)
                auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
                client = Client(account_sid, auth_token)
                if self.order_status == 'ready_to_deliver':
                    message = client.messages.create(
                                    body=f'''\nOrder Shipment Update\n\nDear {self.customer_id.customer_name},\nWe are excited to let you know that your order with id {self.placing_id} has been shipped.\n\nThank you for choosing our service!\nBest regards,\nDekhatis''',
                                    from_=os.environ.get('MY_NUMBER'),
                                    to='+91'+str(self.customer_id.customer_phone),
                                    )
                elif self.order_status == 'shipping':
                    
                    message = client.messages.create(
                                        body=f'''\nDelivery Confirmation\n\nDear {self.customer_id.customer_name},\nWe are pleased to inform you that your order with id {self.placing_id} has been delivered successfully.\n\nThank you for choosing our service!\nBest regards,\nDekhatis''',
                                        from_=os.environ.get('MY_NUMBER'),
                                        to='+91'+str(self.customer_id.customer_phone),
                                )
                else:
                    message = client.messages.create(
                                    body=f'''\ncongratulations!\nYour order with id {self.placing_id} has been successfully placed and is currently being processed.\n\nDear {self.customer_id.customer_name},\nThank you for your order! \nThe estimated delivery time is {self.item_id.item_shipping_time} days.\nplease feel free to contact us at 9354271779 .\n\nThank you for choosing our service!\nBest regards,\nDekhatis''',
                                    from_=os.environ.get('MY_NUMBER'),
                                    to='+91'+str(self.customer_id.customer_phone),
                    )
                print(message)
            except Exception as e:
                print(f"Error: {e}")
        """
        
        return super().save(*args, **kwargs)
    
    class Meta:
        db_table='query_table'

class Images_table(models.Model):
    item_id = models.ForeignKey("Product", verbose_name= "item", default=1, on_delete=models.SET_DEFAULT)
    item_pic1 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic2 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic3 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic4 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic5 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic6 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic7 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic8= models.ImageField(upload_to='uploads/images',blank=True)
    item_pic9 = models.ImageField(upload_to='uploads/images',blank=True)
    item_pic10 = models.ImageField(upload_to='uploads/images',blank=True)
    class Meta:
         db_table='images_table'

class Advertisement_table(models.Model):
    adver_image =models.ImageField(upload_to='uploads/adver_images')
    adver_url =models.CharField(max_length=100,unique=True)
    paid_adver_date=models.DateTimeField(auto_now_add=True ,null=True, blank=True)
    class Meta:
        db_table='advertisement_table'

class Review_table(models.Model):
    item_id= models.ForeignKey("Product", verbose_name= 'reviews',default=1 , on_delete=models.SET_DEFAULT)
    customer_id = models.ForeignKey("Query_table", verbose_name= "customer", default=1, on_delete=models.SET_DEFAULT)
    comments= models.CharField(max_length=400)
    events=models.ImageField(upload_to='uploads/reviews_images',blank=True)
    class Meta:
        db_table='review_table'

class Cancellations_table(models.Model):
    cancellation_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    placing_id= models.ForeignKey("Query_table", verbose_name= "customer", default=1, on_delete=models.SET_DEFAULT)
    shop_id = models.ForeignKey("Shop_table", verbose_name= "shop", default=1, on_delete=models.SET_DEFAULT)
    item_id = models.ForeignKey("Product", verbose_name= "item", default=1, on_delete=models.SET_DEFAULT)
    customer_id=  models.ForeignKey("Customer_table",verbose_name="customer",default=1,on_delete=models.SET_DEFAULT)
    cancellations_date= models.DateTimeField(auto_now_add=True)
    order_date= models.CharField(max_length=50)
    order_status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=200)
    bank_id=models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        """
        try:
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                body=f'''Dear {self.customer_id.customer_name},\nWe have received your cancellation request  with cancellation id {self.cancellation_id} for your recent order with order id {self.placing_id.placing_id}. \n\nWe are sorry to hear that you have changed your mind and hope to serve you better in the future.We will process your cancellation request and refund your payment within 3 days.\nThank you for choosing our service and we look forward to serving you again soon.\n\nBest regards,\nDekhatis''',
                                from_=os.environ.get('MY_NUMBER'),
                                to='+91'+str(self.customer_id.customer_phone),
                            )
         
        except Exception as e:
            print(f"Error: {e}")
        """
        return super().save(*args, **kwargs)
    class Meta:
        db_table='cancellations_table'

class ThemeFurniture(models.Model):
    id =  models.AutoField(primary_key=True)
    theme_cost = models.CharField(max_length=100)
    theme_date = models.DateField(auto_now_add=True) 
    theme_revenue = models.CharField(max_length=100)
    theme_room= models.CharField(max_length=100)
    theme_availability  = models.CharField(max_length=100)
    theme_discount_percentage = models.CharField(max_length=100)
    theme_image = models.ImageField(max_length=100,blank=True,null =True)
    details = models.CharField(max_length=100)
    theme_item_list = models.TextField(blank=True)
    class Meta:
        db_table='theme_table'


class ThemeFurnituresBookings(models.Model):
    id =  models.AutoField(primary_key=True)
    customer_id= models.CharField(max_length=100,blank=True,null =True)
    shop_id=models.CharField(max_length=100,blank=True,null =True)
    placing_id = models.TextField(max_length=100,blank=True,null =True)
    theme_id = models.CharField(max_length=100)
    theme_order_status = models.BooleanField(blank=True,null =True)
    def save(self, *args, **kwargs):
            print('themessave')
            """
            try:
                account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
                print(self.customer_id.customer_name)
                auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
                client = Client(account_sid, auth_token)
                otp = str(random.randint(100000, 999999))
                message = client.messages.create(
                                body=f'''\ncongratulations!\nYour Theme with id {self.id} has been successfully placed and is currently being processed.\n\nDear {self.customer_id.customer_name},\nThank you for your order! \nThe estimated delivery time is {self.item_id.item_shipping_time} days.\n\nOTP: {otp}\n\nPlease use this OTP for verification purposes.\nplease feel free to contact us at 9354271779 .\n\nThank you for choosing our service!\nBest regards,\nDekhatis''',
                                    from_=os.environ.get('MY_NUMBER'),
                                    to='+91'+str(self.customer_id.customer_phone)
                                    )
                print(message)
            except Exception as e:
                print(f"Error: {e}")
            """
            return super().save(*args, **kwargs)
    class Meta:
        db_table='theme_booking_table'

class Dekhatis_Delivery_table(models.Model):
    id =  models.AutoField(primary_key=True)
    delivery_merchant_id=models.CharField(max_length=200,null=True,blank=True)
    order_id = models.CharField(max_length=200,null=True,blank=True)
    delivery_payment = models.IntegerField(null=True,blank=True)
    product_pickup_location = models.CharField(max_length=200,null=True,blank=True)
    product_dropoff_location =models.CharField(max_length=200,null=True,blank=True)
    item_id=models.CharField(max_length=200,null=True,blank=True)
    delivery_merchant_payment =models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        db_table ='dekhatis_delivery_table'

class Wood_Servicing_table(models.Model):
    servicing_placing_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    customer_id= models.ForeignKey("Customer_table", verbose_name= "user",default=1, on_delete=models.SET_DEFAULT)
    shop_id = models.ForeignKey("Shop_table", verbose_name= "shop", default=1,on_delete=models.SET_DEFAULT)
    shop_pin= models.IntegerField()
    service_state= models.CharField(max_length=200,blank=True)
    service_address= models.CharField(max_length=300,blank=True)
    service_pin =models.IntegerField(default=0)
    service_phone= models.CharField(max_length=14,blank=True)
    order_date= models.DateTimeField(auto_now_add=True,null=True, blank=True)
    service_status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=200)
    bank_id=models.CharField(max_length=200,blank=True)
    service_date = models.DateTimeField(null=True, blank=True)
    payment_status =models.CharField(max_length=200,null=True,blank=True)
    dekhatis_payment_status = models.CharField(max_length=200,null=True,blank=True)
    class Meta:
        db_table = 'wood_servicing_table'

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(('The given username must be set'))
        email = self.normalize_email(email)
        user = User(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, password, email=None, **extra_fields):
        return self._create_user(username, email, password, is_staff=False ,is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, password, username='admin', email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser,PermissionsMixin):
    
    phone_number = models.CharField(max_length=12, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
    username = models.CharField(max_length=150, unique=False)
    terms_conditions=models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

class My_Product_ModelAdmin(admin.ModelAdmin):
    search_fields = ['item_id', 'item_name', 'item_categories', 'item_detail', 'item_size', 'item_finish', 'item_storage', 'item_colour', 'item_room', 'item_shipping_time', 'item_visual_similarity', 'item_warrenty', 'item_instructions', 'item_discount_percentage', 'item_availability','shop_id__shop_id', 'shop_pin','shop_id__shop_name']
    list_display = ['item_id', 'item_name', 'item_cost', 'item_availability', 'shop_id']

class My_ShopTableModelAdmin(admin.ModelAdmin):
    search_fields = ['shop_id', 'shop_name', 'shop_brand_name', 'shop_email', 'shop_address', 'shop_phone', 'shop_alt', 'shop_ordered', 'manufacturer_name', 'manufacturer_address', 'manufacturer_phone']
    list_display = ['shop_id', 'shop_name', 'shop_phone', 'shop_pin']

class My_CustomerTableModelAdmin(admin.ModelAdmin):
    search_fields = ['customer_id', 'customer_name', 'customer_email', 'customer_phone', 'customer_pin']
    list_display = ['customer_id', 'customer_name', 'customer_email', 'customer_phone']

class My_Query_table_Admin(admin.ModelAdmin):
    search_fields = ['item_cost']
    search_fields = ['placing_id','customer_id__customer_id', 'shop_id__shop_id','shop_id__shop_pin', 'item_id__item_id','order_date','shipping_otp','transaction_id','payment_status','order_status','dekhatis_payment_status']
    list_display = ['placing_id', 'customer_id', 'shop_id', 'item_id', 'item_cost', 'order_date', 'order_status','payment_status','dekhatis_payment_status']

class My_CancellationsAdmin(admin.ModelAdmin):
    search_fields = ['cancellation_id','placing_id__placing_id','customer_id__customer_id', 'shop_id__shop_id','shop_id__shop_pin', 'item_id__item_id']
    list_display = ['cancellation_id','placing_id', 'customer_id', 'shop_id', 'item_id','order_date', 'order_status']

class My_UserAdmin(admin.ModelAdmin):
    search_fields = ['phone_number', 'username', 'email']
    list_display = ['id', 'phone_number', 'username', 'email', 'is_phone_verified', 'terms_conditions']


class My_review_ModelAdmin(admin.ModelAdmin):
    search_fields = ['item_id','customer_id']
    list_display =['item_id','customer_id']


class My_advertise_ModelAdmin(admin.ModelAdmin):
    search_fields = ['adver_url','paid_adver_date']
    list_display =['adver_url','paid_adver_date']


class My_image_ModelAdmin(admin.ModelAdmin):
    search_fields = ['item_id']
    list_display =['item_id']


class My_ThemeFurnitureAdmin(admin.ModelAdmin):
    search_fields = ['theme_room', 'theme_item_list','theme_discount_percentage',]
    list_display = ['theme_cost', 'theme_room', 'theme_availability', 'theme_date']

class My_ThemeFurnituresBookingsAdmin(admin.ModelAdmin):
    search_fields = ['customer_id', 'shop_id', 'placing_id', 'theme_id']
    list_display = ['id', 'customer_id', 'shop_id', 'theme_id', 'theme_order_status']

class My_Dekhatis_DeliveryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'delivery_merchant_id','order_id','product_pickup_location','product_dropoff_location','item_id','delivery_merchant_payment']
    list_display=['id', 'delivery_merchant_id','product_pickup_location','product_dropoff_location','item_id','delivery_merchant_payment']

class My_Wood_ServicingAdmin(admin.ModelAdmin):
    search_fields = ['servicing_placing_id', 'customer_id__customer_id','shop_id__shop_id','shop_pin','service_state','service_address','service_pin','order_date','service_status','payment_status','dekhatis_payment_status']
    list_display = ['servicing_placing_id', 'customer_id','shop_id','service_state','service_pin','order_date','service_status','payment_status','dekhatis_payment_status']