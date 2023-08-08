
from rest_framework import serializers
from .models import Product, Customer_table, Shop_table, Query_table,Cancellations_table,Review_table,User, ThemeFurnituresBookings, ThemeFurniture, Wood_Servicing_table, Serving_CRM_table, Query_CRM_table,User_CRM_table


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=False)
    otp = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True, write_only=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_phone_verified','otp',
                  'terms_conditions', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'phone_number': {'required': True, 'allow_blank': False},
            'is_phone_verified': {'read_only': True},
            'otp': {'required': True, 'read_only': True},
            'password': {'required': True},
            'email': {},
            'terms_conditions': {},
            'first_name': {},
            'last_name': {},
            'is_superuser': {},
            'is_staff': {},
        }

    def create(self, validated_data):
        extra_fields = {
            'phone_number': validated_data.get('phone_number', ''),
            'otp': validated_data.get('otp', ''),
        }

        myuser = User.objects.create_user(
            username=validated_data.get('username', ''),
            password=validated_data.get('password', ''),
            **extra_fields
        )

        if myuser is None:
            raise serializers.ValidationError('Unable to create user with given data.')

        return myuser



class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_table
        fields = ['id','shop_image','shop_id','shop_name','shop_brand_name','shop_email','shop_phone',
                  'shop_alt','shop_pin','shop_date','manufacturer_name','manufacturer_address','manufacturer_phone','shop_service_availability','item_total_number','woodservicing_register',]


class ProductSerializer(serializers.ModelSerializer):
    shop_id = ShopSerializer()

    class Meta:
        model = Product
        fields = ['item_id','m_item_id','item_name','item_image','item_categories','item_detail','item_availability',
                  'item_cost','shop_pin','shop_id','item_size','item_finish','item_storage','item_colour',
                  'item_room','item_shipping_time','item_visual_similarity','item_warrenty','item_instructions','item_discount_percentage','item_rating','item_delivery_cost','item_recommended']


class VariantSerializer(serializers.ModelSerializer):
    shop_id = ShopSerializer()

    class Meta:
        model = Product
        fields = ['item_id','m_item_id','item_name','item_image','item_categories','item_detail','item_availability',
                  'item_cost','shop_pin','shop_id','item_size','item_finish','item_storage','item_colour',
                  'item_room','item_shipping_time','item_visual_similarity','item_warrenty','item_instructions','item_discount_percentage','item_rating','item_delivery_cost','item_recommended']


class VisualSerializer(serializers.ModelSerializer):
    shop_id = ShopSerializer()

    class Meta:
        model = Product
        fields = ['item_id','m_item_id','item_name','item_image','item_categories','item_detail','item_availability',
                  'item_cost','shop_pin','shop_id','item_size','item_finish','item_storage','item_colour',
                  'item_room','item_shipping_time','item_visual_similarity','item_warrenty','item_instructions','item_discount_percentage','item_rating','item_delivery_cost','item_recommended']


class SearchSerializer(serializers.ModelSerializer):
    shop_id = ShopSerializer()

    class Meta:
        model = Product
        fields = ['item_id','m_item_id','item_name','item_image','item_categories','item_detail',
                  'item_cost','shop_pin','shop_id','item_size','item_finish','item_storage','item_colour','item_availability',
                  'item_room','item_shipping_time','item_visual_similarity','item_warrenty','item_instructions','item_discount_percentage','item_rating','item_delivery_cost','item_recommended']


class ClickedSerializer(serializers.ModelSerializer):
    shop_id = ShopSerializer()

    class Meta:
        model = Product
        fields = ['item_id','m_item_id','item_name','item_image','item_categories','item_detail',
                  'item_cost','shop_pin','shop_id','item_size','item_finish','item_storage','item_colour','item_availability',
                  'item_room','item_shipping_time','item_visual_similarity','item_warrenty','item_instructions','item_discount_percentage','item_rating','item_delivery_cost','item_recommended']


class CustomerSerializer(serializers.ModelSerializer):
    
    customer_name = serializers.CharField(required=True)
    customer_email = serializers.EmailField(required=True)
    customer_state = serializers.CharField(required=True)
    customer_address = serializers.CharField(required=True)
    customer_pin = serializers.IntegerField(required=True)
    customer_phone = serializers.CharField(required=True)

    class Meta:
        model = Customer_table
        fields = ('customer_id', 'customer_name', 'customer_email', 'customer_state', 'customer_address', 'customer_pin', 'customer_phone','customer_status')


class QuerySerializer(serializers.ModelSerializer):
    customer_id = serializers.SlugRelatedField(slug_field='id', queryset=Customer_table.objects.all())
    shop_id = serializers.SlugRelatedField(slug_field='id', queryset=Shop_table.objects.all())
    item_id = serializers.SlugRelatedField(slug_field='item_id', queryset=Product.objects.all())
    class Meta:
        model = Query_table
        customer_name = serializers.CharField(source='customer_id')
        fields = ['placing_id','customer_id','shop_id','item_id','item_cost','item_quantity','delivery_state','shipping_otp',
                  'delivery_address','delivery_pin','delivery_phone','order_date','order_status','transaction_id','bank_id','delivery_date','item_delivery_cost']
        
        def create(self, validated_data):
            instance = Query_table(**validated_data)
            instance.custom_save()
            return instance
            
class CancellationsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Cancellations_table

        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review_table
        fields = '__all__'

class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThemeFurniture
        fields = '__all__'
        
class ThemeBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThemeFurnituresBookings
        fields = '__all__'
    
class Wood_Servicing_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Wood_Servicing_table
        fields = '__all__'

class Serving_CRM_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Serving_CRM_table
        fields= '__all__'


class Query_CRM_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Query_CRM_table
        fields= '__all__'


class User_CRM_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User_CRM_table
        fields= '__all__'