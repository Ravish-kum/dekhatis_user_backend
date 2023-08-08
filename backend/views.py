from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from .models import User, Product, Images_table, Customer_table,Query_table, Review_table,ThemeFurnituresBookings,ThemeFurniture, Shop_table, Wood_Servicing_table, User_CRM_table, Serving_CRM_table
import uuid
from django.conf import settings
from django.core import serializers
import jwt
import datetime
from rest_framework.decorators import authentication_classes
from django.http import JsonResponse, HttpResponse,Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login,get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProductSerializer, UserSerializer, VariantSerializer, VisualSerializer, SearchSerializer, ClickedSerializer,Wood_Servicing_Serializer,CustomerSerializer,  QuerySerializer,QuerySerializer,CancellationsSerializer, ReviewSerializer,ThemeSerializer,ThemeBookingSerializer, User_CRM_Serializer, Serving_CRM_Serializer
User = get_user_model()
from django.db.models import Q
from django.utils import timezone
import logging, traceback
logger = logging.getLogger('my_web')
from decimal import Decimal
import random
from .task import query_crm, serving_CRM_count
from django.db.models import F

#===============================================================================================================================================================
#==============================================================authentications==================================================================================
''' function used for fetching jwt access and refresh tokens from authentications headers '''

def get_payload_from_token(authorization_header):
    secret_key = settings.SECRET_KEY

    if authorization_header is None:
        logger.info('Authorization header is missing')
        return None, Response({'error': 'Authorization header missing',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        access_token = authorization_header.split(' ')[1]
    except IndexError:
        return None, Response({'error': 'Invalid Authorization header',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        data = jwt.decode(access_token, secret_key, algorithms=['HS256'])['payload']
        access_token_payload = json.loads(data)
        payload = access_token_payload[0]['pk']
        logger.info('payload successfully formed')

    except jwt.exceptions.InvalidSignatureError:
        return None, Response({'error': 'Invalid token signature',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.DecodeError:
        return None, Response({'error': 'Invalid token format',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

    return payload, None


#================================================================================================================================================
'''class signup creates a user by taking phone number, username, password, otp.
    if user already exists : 'user already exists' 
    if invalid credentials : "invaild credentials" 
    successful signup      : 'signup successful' '''

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        phone_number = request.data.get('phone_number')
        already_exist = User.objects.filter(phone_number=phone_number).exists()
        
        if already_exist == True:
            logger.info('user already existed')
            return Response({'error': 'user already exists','status_code':409})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            logger.info("successfully became a new user")

        except Exception as e :
            logger.info('failed to save new user - error %s',str(e))
            return Response({"error":"invalid credentials",'status_code':400})
        

        return Response({
            'message':'signup successful',
            'status_code': 200
        })


@csrf_exempt
def signup(request):
    view = SignupView.as_view()
    response = view(request)
    return response

#================================================================================================================================================
"for POST method "
''' class signin authenticate the user and give access and refresh token by taking phone number and password 
    and his phone number will be authenticated by javascript - firebase authentications 
    
    if user does not exist or worng password :'not a user or wrong phone number' 
    if user exist : 'signin success' '''

"for GET method "
''' takes bearer token and give the profile of the user 
    
    if no authentucations headers : 'Customer ID not found in token payload' 
    success : 'detailed view' '''

class Signin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        
        myuser = authenticate(phone_number=phone_number, password=password)
        
        already_exist = User.objects.filter(phone_number=phone_number).exists()
        if not already_exist:
            logger.info("not a user")
            return Response({'error': 'not a user or wrong phone number','status_code':409})
        if myuser is not None:
            logger.info("successfully authenticated a user")
            user_id_dict = User.objects.values('id').filter(phone_number=phone_number).first()
            user_id = user_id_dict['id']
            user = User.objects.get(id=user_id)

            refresh_token = RefreshToken.for_user(user)
            access_token_payload = serializers.serialize('json', [user, ])
            access_token = refresh_token.access_token
            access_token['payload'] = access_token_payload
            login(request, myuser)
            logger.info("successfully user login")
            
            return Response({
                'message':'signin success',
                'status_code':200,
                'refresh_token': str(refresh_token),
                'access': str(access_token), })

        else:
            logger.info('invalid credentials')
            return Response({'error': 'Invalid password',"status_code":400})
        
    def get(self, request):
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info("error from paload function in sigin/get %s ",str(error_response))
            return error_response

        # Extract the customer ID from the payload
        if not payload:
            logger.info("error in getting payload in sigin/get")
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_details = User.objects.get(id=  payload)
            serializer = UserSerializer(user_details)
            logger.info("successfully got user details")
        except Exception as e :
            logger.info("error in getting user %s",str(e))
            return Response({'error':'internal server error','status_code':500})
        return Response({'message':serializer.data,'status_code':200})
 
#================================================================================================================================================
''' class forget password make user able to change his password by provinding his phone number and new password '''
''' if user does not exists : "user does not exist" 
    success : 'Password updated successfully' '''

class ForgotPassword(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        new_password = request.data.get('new_password')
        
        try:
            user = User.objects.get(phone_number=phone_number)
            logger.info("got user who is trying to change the password")
        except User.DoesNotExist:
            logger.info("error not a user who is trying to change the password")
            return Response({'error':"user does not exist", 'status_code':409})
        
        user.set_password(new_password)
        user.save(update_fields=['password'])
        logger.info("successfully set new password")
        return Response({'message': 'Password updated successfully','status_code':200})
    
#===============================================================================================================================================================
#==============================================================products=========================================================================================
''' class gettingproducts gives every products and its details in response except those having item_availability deleted
    if success : 'all products listed' 
    if empty : "Product list is empty" '''

class Gettingproducts(generics.ListAPIView):
    def get(self, request):
        try:
            products = Product.objects.exclude(item_availability='deleted')
            serializer = ProductSerializer(products, many=True)
            logger.info("successfully got all products")
        except Product.DoesNotExist:
            logger.info("error in getting products")
            return Response({'error':"Product list is empty", 'status_code':409})
        
        return Response({"message":"all products listed","products":serializer.data,'status_code':200})

#================================================================================================================================================================
''' class gettingdescriptions give details of perticular product by getting myid ( item_id ) and get visualsimilars, images, recommended, varients
    by excluding deleted ones'''

class GettingDescription(generics.ListAPIView):
    def get(self, request, myid):

        getting_the_clicked_product = Product.objects.filter(item_id=str(myid)).exclude(item_availability='deleted')
        try:
            print(getting_the_clicked_product)
            if getting_the_clicked_product.exists():
                serializer = ProductSerializer(getting_the_clicked_product, many=True)
                logger.info("successfully got the clicked product for description")
            else:
                logger.info("Product not found for the given ID")
                return Response({"error": "Product not found", "status_code": 409})

    # here we get discriptions in serializer
        except Exception as e:
            logger.info('failed to get product from click - error %s',str(e))
            return Response({"error": "product not found","status_code":409})
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
        try:
            m_item_id_of_product = Product.objects.values('m_item_id','item_recommended','item_visual_similarity').filter(item_id=myid).exclude(item_availability='deleted').first() 
            print(m_item_id_of_product)
            logger.info("successfully got m_item_id of clicked product")
            # m_item_id_of_product getting varients
        except Exception as e:
            logger.info('failed to get varient_id of a product %s - error %s',str(myid),str(e))
            return Response({'error':"variant is not mentioned", 'status_code':500})

        check = m_item_id_of_product['m_item_id']
        if check is not None and check != '':
            variant_of = check.split("#")[2]
            try:
                variant = Product.objects.filter(m_item_id__icontains=variant_of).exclude(item_id=str(myid)).exclude(item_availability='deleted')
                if variant.exists():
                    variant_serializer = VariantSerializer(variant, many=True)
                    variant_serializer= variant_serializer.data
                    logger.info("successfully got varients of clicked product")
                else:
                    logger.info("no varient for the given ID")
                    variant_serializer = []
    #here we get variants of that product in varient_serializer

            except Exception as e:
                logger.info('failed to get varients of a product %s - error %s',str(myid),str(e))
                variant_serializer = []
        else:
            variant_serializer = []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
        check_similar = m_item_id_of_product['item_visual_similarity']
        if check_similar is not None and check != '':
            
            try:
                visualsimilar = Product.objects.filter(item_visual_similarity=check_similar).exclude(item_id=myid).exclude(item_availability='deleted')
                if visualsimilar.exists():
                    visualsimilar_serializer = VisualSerializer(visualsimilar, many=True)
                    visualsimilar_serializer = visualsimilar_serializer.data
                    print(visualsimilar)
                    logger.info("successfully got visualsimilar of clicked product")
                else:
                    logger.info("no visual similar for the given ID")
                    visualsimilar_serializer = []
    #here we get visualsimilars in visualsimilar_serializer

            except Exception as e:
                logger.info('failed to get visual similar products - error %s',str(e))
                visualsimilar_serializer = []
        else:
            visualsimilar_serializer = []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
        check_recommended = m_item_id_of_product['item_recommended']
        if check_recommended is not None and check != '':
            try:
                recommended = Product.objects.filter(item_recommended=check_recommended).exclude(item_id=myid).exclude(item_availability='deleted')
                if recommended.exists():
                    recommended_serializer = VisualSerializer(recommended, many=True)
                    recommended_serializer = recommended_serializer.data
                    logger.info("successfully got recommended products of clicked product")
                else:
                    logger.info("no recommended for the given ID")
                    recommended_serializer = []
    #here we get recommmended products in recommended_serializer

            except Exception as e:
                logger.info('failed to get recommended products - error %s',str(e))
                recommended_serializer = []
        else:
            recommended_serializer = []
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        subject_images = Images_table.objects.filter(item_id=myid)
        images_url = []
        for i in subject_images:
            for attr, value in i.__dict__.items():
                if value != "":
                    images_url.append(value)
        if images_url:
            del images_url[0:3]
        logger.info("successfully got images url")
        crm_param=getting_the_clicked_product.values()
        serving_CRM_count(category=crm_param[0]['item_categories'])
        serving_CRM_count(cost=crm_param[0]['item_cost'])
        serving_CRM_count(item_id_for_desc=crm_param[0]['item_id'])
    
        
        
    #here we get urls of side images of products to display 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        return Response({
            "message":"description - variant - visualsimilar - image_urls - recommended",
            'description': serializer.data,
            'recommended':recommended_serializer,
            'variant': variant_serializer,
            'visualsimilar': visualsimilar_serializer,
            'image_urls': images_url,
            'status_code':200
        })

#================================================================================================================================================
''' class productsearch is for search bar and icons to reach on categories page '''
"for GET method "
'it takes a parameter clicked id (item_categories) and give list of same category products as result '

"for POST method "
'it get searching word from search bar and search the presence of the word in item_name to give list of products having keyword in thier name '

class ProductSearch(APIView):
    def get(self, request, clicked_id):
        serving_CRM_count(category=clicked_id)
        # clicked_id = request.query_params.get('clicked_id')
        try:
            product1 = Product.objects.filter(item_categories=clicked_id).exclude(item_availability='deleted').first()
            if product1 is None:
                logger.info("no clicked product found")
                return Response({"error": "product not found","status_code":409})
            
            product = Product.objects.filter(item_categories=clicked_id).exclude(item_availability='deleted')
            serializer = ClickedSerializer(product, many=True)
            logger.info("successfully got clicked product")
            
            return Response({"message":"products by id clicked on icons",'clicked': serializer.data,'status_code':200})
        except Exception as e:
            logger.info('failed to get products from click - error %s',str(e))
            return Response({"error": "product not found by internal issue","status_code":500})
        
        

    def post(self, request):
        categoryfilter = request.data.get('searched_id')
        serving_CRM_count(search = categoryfilter)
        try:
            productcheck = Product.objects.filter(item_name__icontains=categoryfilter).exclude(item_availability='deleted').first()
            if productcheck is None:
               logger.info("no searched product found")
               return Response({"error": "product not found","status_code":409})
            else:
                product = Product.objects.filter(item_name__icontains=categoryfilter).exclude(item_availability='deleted')
                serializer = SearchSerializer(product, many=True)
                logger.info("successfully got searched product")
                
            return Response({"message":"products by searched on search bar",'searched': serializer.data,'status_code':200})
        except Exception as e:
            logger.info('failed to get products from search - error %s',str(e))
            return Response({"error": "product not found by internal issue","status_code":500})

#===================================================================================================================================================
''' class roomfilters give the filter of product having similar room ans item_room '''

class Roomfilters(APIView):
    def get(self,request,room):
        serving_CRM_count(category=room)
        try:
            product_by_room = Product.objects.filter(item_room=room).exclude(item_availability='deleted').first()
            if product_by_room is None:
               logger.info("No product with roomfilter")
               return Response({"error": "product not found","status_code":409})
            
            product_by_room = Product.objects.filter(item_room=room).exclude(item_availability='deleted')
            serializer = ProductSerializer(product_by_room, many=True)
            logger.info("product with roomfilter")
            return Response({"message":"products by room filter icons",'clicked': serializer.data, "status_code":200})
        
        except Exception as e:
            logger.info('failed to get products from same room - error %s',str(e))
            return Response({"error": "products not found be internal issue",'status_code':500})
        
#====================================================================================================================================================
'''class theme display give the list of themes available excluding the deleted ones '''

class ThemeDisplay(APIView):
    def get(self,request):
        try:
            themes = ThemeFurniture.objects.exclude(theme_availability='deleted')
            serializer = ThemeSerializer(themes,many= True)
        except Exception as e:
            logger.info('failed to get themes - error %s',str(e))
            return Response({"error": "themes are not available",'status_code':409})
        
        logger.info("successfully got all themes")
        return Response({
            'message':'list of themes',
            'themes':serializer.data,
            'status_code':200
        })

#=====================================================================================================================================================
''' class themediscriptiondisplay give the discriptive view of a perticular theme by having its id in parameter'''

class ThemeDiscriptionsDisplay(APIView):
    def get(self,request,id):
        
        try:
           themes = ThemeFurniture.objects.exclude(theme_availability='deleted').get(id =id)
        except ThemeFurniture.DoesNotExist:
            logger.info("no themes available")
            return Response({"error":"theme not found","status_code":409})
        
        serializer = ThemeSerializer(themes)
        logger.info("successfully got all themes")
        return Response({
            'themes':serializer.data,
            'status_code':200
        })

#=======================================================================================================================================================
''' theme booking is a funtion which is called during the process of theme booking
    when someone books a theme it runs the checkout simpling booking all item listed in theme and 
    after booking all item separatly checkout trigger this funcions to distinguish theme booking from cart booking'''
'''function generates a query having all order items placing id (placing_id), theme_id and shop id list (shop_id)'''

def themebooking(theme_placing_id_dict, theme_id,customer_id, theme_shop_id_list):
   
    data= {
        'placing_id':str(theme_placing_id_dict),'theme_id':theme_id,'customer_id':customer_id,'shop_id':','.join(map(str, theme_shop_id_list)),
    }
    
    serializer =  ThemeBookingSerializer(data=data) 
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        logger.info("themes booking saved")
    return Response({
        'data':serializer.data,
        'status_code':200
    })

#===============================================================================================================================================================
#==============================================================customer_creations======================================================================================
''' class customercreation is for more details about the user asked before every booking which includes "customer_name","customer_otp",
    "customer_email","customer_address","customer_pin","customer_city","customer_phone","customer_state" '''

" for Get method "
''' gives profile of the customer with all detailed he filled by using authentication tokens 
        'if not authentication token : Customer ID not found in token payload'
        'if authentications token : successfully customer display' '''

" for POST method "
''' gives ability to change the his details or to become a new customer 
    if new customer : successfuly customer formed
    if already exist : successfuly customer updated '''

''' customer creations is different from user formation as user is formed with less details to access the different authenticated views 
    customer is created to one responsible for booking done by the user'''

class CustomerCreations(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        
        if error_response:
            logger.info('failed to get payload %s',str(error_response))
            return error_response

        # Extract the customer ID from the payload
        if not payload:
            logger.info("failed to get payload")
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)

        customercheck = Customer_table.objects.filter(customer_id=payload)
        serializer = CustomerSerializer(customercheck, many=True)
        customer_identity = serializer.data
        if not customer_identity:
            logger.info('failed to get customer')
            return Response({"error":'not our customer',"status_code":400}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            {'customer': customer_identity,
             'message':"successfully customer display",
             'status_code': 200
            }
        )
    def post(self, request):
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info('failed to get themes - error %s',str(error_response))
            return error_response

        # Extract the customer ID from the payload
        if not payload:
            logger.info('failed to get payload')
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        serving_CRM_count(checkout_view_count=True)
        already_exist = Customer_table.objects.filter(customer_id=payload).exists()

        if already_exist:
            logger.info('customer already exist')
            customer_instance = Customer_table.objects.get(customer_id=payload)
            
            serializer = CustomerSerializer(customer_instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(customer_id=payload)
                logger.info('customer updated')
                return Response({"message":"successfuly customer updated","status_code":200})

            else:
                logger.info('server error %s',serializer.errors)
                return Response({"error":serializer.errors,"status_code":400}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            customer_serializer = CustomerSerializer(data=request.data)

            if customer_serializer.is_valid(raise_exception=True):

                customer_serializer.save(customer_id=payload)
                customer_serializer.save()
                logger.info('New customer save')

                return Response({"message":"successfuly customer formed","status_code":200})

            else:
                logger.info('server error %s',customer_serializer.errors)
                return Response({"error":customer_serializer.errors,"status_code":400}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def customercreations(request):
    view = CustomerCreations.as_view()
    response = view(request)
    return response
#=================================================================================================================================================================
#==============================================================checkout============================================================================================
''' 
class checkouts are for placing orders which includes two types of checkouts first - cart_item checkouts and secondly theme_cart checkouts

"cart checkout"
    step 1 : customer must be formed from Class CustomerCreations 
    step 2 : for check out dict of item_id which is selected in cart must be sended to the backend with variable name {originalcart} with quantity eg :"originalcart":{"i1": 1,"i3": 1}
    step 3 : stored original_cart values in cart_item variable which is then equated to item_dict for loop
    step 4 : there will be a check of every item_id's - availablity 
                                                            NON AVAILABLE PRODUCTS ID'S COLLECTED AND OTHERS ARE BOOKED
                                                        and existence
                                                            NON EXISTING BREAKS THE LOOP AND RESPONSE ERROR 
    step 5 : for loop will run and every item id product will be booked with multiple confirmation message in normal save by filling out every required row
                in query table

"theme checkouts"
    step 1 : customer must be formed from Class CustomerCreations 
    step 2 : for check out dict of item_id which is devoted to theme must be sended to the backend with variable {themecart} and its quantity eg: "themecart":{"i1": 1,"i3": 1}, 
    step 3 : then themeid must be sended eg: "themeid":1 
    step 4 : stored theme_cart values in theme_cart variable which is then equated to item_dict for loop
    step 5 : there will be a check of every item_id's - availaiblity and existence
                                                        NON AVAILABLITY OR NON EXISTENCE BREAKS THE LOOP WITH 'SOME ITEMS OF THEME NOT AVAILABLE NOW' ERROR
    step 6 : for loop will run and every item id product will be booked with a single confirmation message in custom save by filling out every required row
                in query table
    step 7 : dict of item_id as key and placing id as values is stored in 'theme_placing_id_dict' variable
    step 8 : list of shop_id who's products are booked are collected in list 'theme_shop_id_list' variable
    step 9 : simultaneous to the booking of all items a themebooking functions save theme order to distinguish it from cart order
    step 10 : customer details is the final response 
    '''

class Checkout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info('failed to get payload - error %s',str(error_response))
            return error_response
        # Extract the customer ID from the payload
        if not payload:
            logger.info('failed to get payload')
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

        theme_id = None
        cart_items = None
        theme_cart = None
        cart_items = request.data.get('originalcart')
        theme_cart = request.data.get('themecart')
        
        if cart_items:
            item_dict =cart_items
            logger.info('cart_items set to item_dict')
        # if there is cart booking then dictionary (cart_items) containing item_id and quantity become equal to item_dict

        elif theme_cart:
            item_dict = theme_cart
            logger.info('theme_cart set to item_dict')
        # if there is theme booking then dictionary (theme_cart) containing item_id and quantity become equal to item_dict

            theme_id = request.data.get('themeid')
            
            if theme_id:
                logger.info('got theme_id')
                theme_check = ThemeFurniture.objects.filter(id = str(theme_id)).exclude(theme_availability='deleted').exists()
                if not theme_check:
                    logger.info('theme_id is not present')
                    return Response({"error":"theme id is not present","status_code":400})
            else:
                logger.info('theme_id not got')
                return Response({"error":"theme id is not given","status_code":400})
        else:
            logger.info('your cart is empty')
            return Response({"error":"your original cart is empty","status_code":400})

    # making item_dict for appling loop for booking 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

        delivery_details = Customer_table.objects.filter(customer_id=payload).values('customer_state','customer_address','customer_pin','customer_phone')

        customer_id_id = Customer_table.objects.get(id= payload)

        customer_id_check = User.objects.filter(id=payload).values('id')
        customer_id = customer_id_check[0]['id']
        single_otp = str(random.randint(100000, 999999))

        # customer_id_id is customer object 
        # #customer_id is true id 
        # delivery_details are used for making query (order)
        # buying is order id 
        # shop_id_id is shop object whose item is booking
    #-------------------------------------------------------------------------------------------------------------------------------------------------

        not_available =[]
        theme_placing_id_dict={}
        theme_shop_id_list =[]
        # list not_available for separate out not availables items and list theme_shop_id_list and dict theme_placing_id_dict for passing to themebooking

        for my_cart_item_id in item_dict.keys(): 

            try:
                item_presence_check = Product.objects.filter(item_id=my_cart_item_id).exclude(item_availability='deleted').exists()
                if not item_presence_check:
                    logger.info('item checked is not present in our list')
                    return Response({"error":"item checked is not present in our list","status_code":500})
            except Exception as e :
                logger.info('failed to get the product cause not in list - error %s',str(e))
                return  Response({"error":"something went wrong" ,"status_code":500})
            
            #product existence check
            #-----------------------------------------------------------------------------------------------------------------------------------------

            try:
                item_availabilty_check = Product.objects.filter(item_id=my_cart_item_id).exclude(item_availability='deleted').values('item_availability') 

                if item_availabilty_check[0]['item_availability'] != 'True':
                    if cart_items != None:
                        not_available.append(my_cart_item_id)
                        logger.info('item in the list is not available and booking is cart based')
                        continue
                    elif theme_cart != None :
                        logger.info('item in the list is not available and booking is theme based')
                        return Response({
                            "error":"some items of the theme are not available now",
                            "status_code":404
                        })
            except Exception as e :
                logger.info('failed to get the product cause not available - error %s',str(e))
                return  Response({"error":"something went wrong" ,"status_code":500})
            
            #product availability check
            #-------------------------------------------------------------------------------------------------------------------------------------------------
            otp = str(random.randint(100000, 999999))
            try:
                buy_item = Product.objects.exclude(item_availability='deleted').get(item_id=my_cart_item_id)
                serializer = ProductSerializer(buy_item)
                logger.info('Product object to booked')
            except Exception as e:
                logger.info('failed to get the product after all checks - error %s',str(e))
                return Response({"error":"something went wrong" ,"status_code":500})
            # buy item is the main available, existed product object
            
            
            buying_id = uuid.uuid4()
            refernce_shop_id = serializer['shop_id']['id'].value
            shop_id_id = Shop_table.objects.get(id= refernce_shop_id)
            order_id = str(buying_id)
 
            if theme_cart:                              # data type object for theme
                customer_id_q = customer_id_id
                shop_id = shop_id_id
                item_id = buy_item
                shipping_otp = single_otp
                logger.info('foreign keys by theme')
            elif cart_items:                            # data type values for cart
                customer_id_q = str(customer_id)
                shop_id = serializer['shop_id']['id'].value
                item_id = serializer['item_id'].value
                shipping_otp = int(otp)
                logger.info('foreign keys by cart')

            else:
                return Response({"error":"something went wrong" ,"status_code":500})
            item_cost = serializer['item_cost'].value*item_dict[my_cart_item_id]
            item_quantity = item_dict[my_cart_item_id]
            delivery_state = delivery_details[0]['customer_state']
            delivery_address = delivery_details[0]['customer_address']
            delivery_pin = delivery_details[0]['customer_pin']
            delivery_phone = delivery_details[0]['customer_phone']
            order_status = 'True'
            transaction_id = 0
            bank_id = 0
            
            if serializer['item_delivery_cost'].value:
                item_delivery_cost = Decimal(serializer['item_delivery_cost'].value)
            else:
                item_delivery_cost = 0
            data = {'placing_id': order_id, 'customer_id': customer_id_q, 'shop_id': shop_id, 'item_id': item_id, 'item_cost': item_cost,
                    'item_quantity': item_quantity, 'order_status': order_status, 'transaction_id': transaction_id,"shipping_otp":shipping_otp,
                    'delivery_state': delivery_state, 'delivery_address': delivery_address, 'delivery_pin': delivery_pin, 'delivery_phone': delivery_phone,
                    'bank_id': bank_id,'item_delivery_cost':item_delivery_cost}
            
            # formation of query table
            #-----------------------------------------------------------------------------------------------------------------------------------------------

            try:
                if theme_cart: 
                    theme_placing_id_dict[serializer['item_id'].value] = order_id
                    logger.info('adding placing_id and item_id in dictionary')
                            # adding placing id in dict theme_placing_id_dict
                    theme_shop_id_list.append(serializer['shop_id']['id'].value)
                    logger.info('adding shop_id in list')
                            # adding shop id in list theme_shop_id

            except Exception as e:
                logger.info('failed to detect theme_cart - error %s',str(e))
                return Response({"error":"somthing went worng","status_code":500})
            
            # adding details to distinguish theme
            #--------------------------------------------------------------------------------------------------------------------------------------------------

            booking_serializer = QuerySerializer(data=data)
            if cart_items:
                if booking_serializer.is_valid(raise_exception=True):
                    booking_serializer.save()
                    logger.info('order placed by cart')
                    # saving all orders from cart by for loop which will send one opt for every product booked

                else:
                    return Response({"error": serializer.errors, "status_code": 400}, status=status.HTTP_400_BAD_REQUEST)
            elif theme_cart:
                booking_instance = Query_table(**data)
                booking_instance.custom_save()
                logger.info('order placed by theme')
                # saving all orders from theme by custom save function to send a single otp for theme booking

            else:
                logger.info('server error %s',str(serializer.errors))
                return Response({"error":serializer.errors,"status_code":400}, status=status.HTTP_400_BAD_REQUEST)
            
            query_crm(item_id=serializer['item_id'].value)
            query_crm(shop_id=serializer['shop_id']['id'].value)
            query_crm(category= serializer['item_categories'].value)
            query_crm(item_cost=serializer['item_cost'].value)
            query_crm(date_time=datetime.datetime.now())
            query_crm(checkout_pincode=serializer['shop_pin'].value)
            query_crm(customer_id=str(customer_id))
       
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if theme_id is not None:
            themebooking(theme_placing_id_dict,theme_id,customer_id,theme_shop_id_list)
            logger.info('themebooking function calling')
            # calling themebooking function to add a theme order having a dict of placing ids and list of shop ids and customer id

        customercheck = Customer_table.objects.filter(customer_id=payload)
        serializer = CustomerSerializer(customercheck, many=True)
        customer_identity = serializer.data

        if len(not_available) != 0:
            logger.info('check of not avilable items')
            error_found="these are gone out of stock {}".format(not_available)
        else:
            error_found = None
        
        
        logger.info("successfully booked all items")
        return Response(
            {'customer': customer_identity,
             'message':"successfully booked items",
             'error':error_found,
             'status_code': 200
            }
        )


#=====================================================================================================================================================================
# function serve_image works to get url and have a pic from that directory

def serve_image(request, image_path):
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image/jpeg')

#====================================================================================================================================================================
#==================================================================profile===========================================================================================
''' class profile work for updating customer(patch), deleting customer(delete) and to get his previous order(get) by taking authentications headers '''

class Profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
    
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info('failed to get payload %s',str(error_response))
            return error_response

        if not payload:
            logger.info('failed to get payload')
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            instance = Customer_table.objects.filter(customer_id=payload).first()
        
            if instance is None:
                logger.info('no customer found')
                return Response({"error":"no customer found","status_code":409})
            
            elif instance.customer_status =='False':
                logger.info('already deleted customer')
                return Response({"error":"already deleted customer","status_code":409})
            
            else:
                instance.customer_status = 'False'
                instance.save()
            
            logger.info('deactivated account succesfully')
            return Response({"message": "deactivated account succesfully","status_code":200})
        
        except Exception as e:
            logger.info('failed to get the user instance to delete - error %s',str(e))
            return Response({'error': "something went wrong","status_code":500})

#===================================================================================================================================================

    def get(self,request):
        
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info('failed to get payload %s',str(error_response))
            return error_response

        if not payload:
            logger.info('failed to get payload')
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        booked_items =None
        booked_themes =None
        try:
            ordered_items = Query_table.objects.filter(Q(customer_id_id=payload) & (Q(order_status=True) | Q(order_status='ready_to_deliver') | Q(order_status= 'cancelled')| Q(order_status= 'delivered')))
            serializers = QuerySerializer(ordered_items, many = True)
            booked_items= serializers.data
            logger.info('your all ordered items')
        except Exception as e:
            logger.info('failed to get the order items or no order items - error %s',str(e))
            return Response({"error":"no booked items","status_code":409})

        try:
            ordered_themes = ThemeFurnituresBookings.objects.filter(customer_id=payload)
            serializers2 = ThemeBookingSerializer(ordered_themes, many = True)
            booked_themes= serializers2.data
            logger.info('your all ordered themes')

        except Exception as e:
            logger.info('failed to get the themes booked or there is no theme booked - error %s',str(e))
            return Response({"error":"no booked themes","status_code":409})
    
        return Response({"booked_items":booked_items,
                         "booked_themes":booked_themes,
                         "message":"all booked items",
                         "status_code":200})
                    
#====================================================================================================================================================
#============================================================cancellations_table=====================================================================
''' cancellations_model is a functions which has ability to cancel single order at a time so it is called differently in theme cancellations and order cancellations
'it takes a placing id in cancellations_request and cancel the order by setting order_status - cancelled'

"order cancellations" 
    one order id is send to this function as parameter and this function create a new row in cancellations_table and set order_status cancelled

"theme cancellations"
    cancellations model function is called multiple time in for loop by giving order id as parameter and this function create a new row in cancellations_table 
    and set order_status cancelled
'''

def cancellations_model(cancellations_request):
    print(cancellations_request)
    cancellations_table_values = Query_table.objects.values('shop_id_id','item_id_id','customer_id_id','order_date','order_status','transaction_id','bank_id').filter(placing_id= cancellations_request).exclude(order_status='delivered').first()
    print(cancellations_table_values)
    if cancellations_table_values is None:
        logger.info('failed to get order from cancellation_request')
        return Response({"error":"no booked items","status_code":409})
    order_date_value= cancellations_table_values["order_date"].strftime("%Y-%m-%d %H:%M:%S")
    placing_id= cancellations_request
    shop_id =cancellations_table_values["shop_id_id"]
    item_id =cancellations_table_values["item_id_id"]
    Customer_id=cancellations_table_values["customer_id_id"]  
    order_date=order_date_value
    order_status = "cancelled"
    transaction_id =cancellations_table_values["transaction_id"]
    bank_id=cancellations_table_values["bank_id"]
    
    data ={'placing_id':placing_id,'shop_id':shop_id,'item_id':item_id,'customer_id':Customer_id,'order_date':order_date,'order_status':order_status,'transaction_id':transaction_id,'bank_id':bank_id}

    serializer = CancellationsSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        logger.info('successfully cancelled order')
    else:
        return Response({"error":serializer.errors, "status_code":400}, status=status.HTTP_400_BAD_REQUEST)
    try:
        product_cancel_update= Query_table.objects.filter(placing_id= cancellations_request)
        product_cancel_update.update(order_status='cancelled')
    except Exception as e:
        logger.info('failed to failed to update a order to cancelled - error %s',str(e))
        return Response({"error":"something went worng","status_code":500})
    
    logger.info("successfuly cancelled the order")
   
#=============================================================================================================================================================
''' class cancellation works to cancel order by calling cancellation_model and passing order_id with name cancellations_request as parameter '''

class Cancellations(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info('failed to get payload %s',str(error_response))
            return error_response

        if not payload:
            logger.info('failed to get payload')
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            cancellations_request = request.data.get('cancellations_request') 
        except Exception as e:
            logger.info('failed to get the order from the placing id in cancellations_request - error %s',str(e))
            return Response({"error":"wrong placing request","status_code":404})
        
        print(payload)
        try:
            ordered_items = Query_table.objects.filter(customer_id_id = payload, placing_id =str(cancellations_request),order_status='True').first()
            print(ordered_items)
        except Exception as e:
            logger.info('failed to failed to update a order to cancelled - error %s',str(e))
            return Response({"error":"wrong cancellation request","status_code":404})
        if ordered_items is None:
            logger.info('no booked items or wrong placing request')
            return Response({"booked_items":"no booked items or wrong placing request","status_code":409})
        else:
            logger.info('calling of cancellation function from cancellations')
            cancellations_model(cancellations_request)
            
        return Response({"message":"order cancelled","status_code":200})
    
#=============================================================================================================================================================
''' class themecancellation works to cancel list of order added in theme by calling cancellation_model and passing order_id with name 
    cancellations_request as parameter by using loop'''

class ThemeCancellations(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            theme_cancellations_request = request.data.get('theme_cancellations_request') 
        except Exception as e:
            logger.info('failed to get the order with placing id in a theme for loop - error %s',str(e))
            return Response({"error":"wrong placing request","status_code":404})
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info('failed to get payload %s',str(error_response))
            return error_response

        if not payload:
            logger.info('failed to get payload')
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
       
    #=============================================================================================================================================
        theme_check = ThemeFurnituresBookings.objects.filter(id=theme_cancellations_request).first()
        if theme_check is None:
            logger.info('not ordered theme cancellation request')
            return Response({'error':'requested theme to cancel is not available','status_code':400})
        
    #=============================================================================================================================================

        object_of_placing_id = ThemeFurnituresBookings.objects.values('placing_id').filter(id=theme_cancellations_request)
        dict_of_placing_id =dict(eval(object_of_placing_id[0]['placing_id']))
        print(dict_of_placing_id)
        for i in dict_of_placing_id.keys():
            # for loop with i value of placing id's
            q = Q(order_status=True) | Q(order_status='ready_to_deliver')
            ordered_items = Query_table.objects.filter(customer_id=payload, placing_id=dict_of_placing_id[i]).exclude(order_status='cancelled').first()
            print(ordered_items)
            if ordered_items is None:
                logger.info('no booked items or wrong placing request')
                return Response({"booked_items":"no booked theme or wrong placing request","status_code":409})
            else:
                logger.info('calling of cancellation function from themecancellations')
                cancellations_model(dict_of_placing_id[i])

        object_of_placing_id.update(theme_order_status=False)
        logger.info('updated theme status false')
        return Response({"message":"theme cancelled","status_code":200})
    
#=================================================================reivews_table=============================================================================
#===========================================================================================================================================================
''' class is for adding review to a product'''
class Reviews(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request,get_id):
        
        payload, error_response = get_payload_from_token(request.META.get('HTTP_AUTHORIZATION'))
        if error_response:
            logger.info('failed to get payload %s',str(error_response))
            return error_response

        if not payload:
            logger.info('failed to get payload')
            return Response({'error': 'Customer ID not found in token payload',"status_code":401}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            item= Product.objects.filter(item_id= get_id).first()
            if item is None:
                return Response({"message":"no item found","status_code":409})
            logger.info('got item for review')

        except Exception as e :
            logger.info('failed to get the product for review - error %s',str(e))
            return Response({"message":"no product found","status_code":409})
        try:
            customer= Query_table.objects.filter(customer_id= payload).filter(item_id= get_id).first()
            if customer is None:
                return Response({"message":"no booked item found","status_code":409})
            logger.info('got customer who is reviwing')
        except Exception as e :
            logger.info('failed to get the customer with item booked - error %s',str(e))
            return Response({"message":"no customer found","status_code":409})
        
        serializer = ReviewSerializer(data=request.data) 
      
        if serializer.is_valid(raise_exception=True):
            serializer.save(customer_id= customer, item_id= item)
            logger.info('successfully set the review')
            return Response({"message":"success","status_code":200})
        else :
            logger.info('some thing went worng in setting review')
            return Response({"message":"invalid try","status_code":400})






from backend.task import serving_CRM_count, User_CRM_count
def CRM_Cart_item_call(request,cart_item_id=None):
    try:
        serving_CRM_count(item_id_for_cart=cart_item_id)
    except Exception as e :
        print(e)
    return HttpResponse('success')


    
def CRM_User_call(request):
    age= request.GET.get('age')
    gender= request.GET.get('gender')
    income_level= request.GET.get('income_level')
    pincode= request.GET.get('pincode')
    if age:
        User_CRM_count(age=age)
    elif gender:
        print(gender)
        User_CRM_count(gender=gender)
    elif income_level:
        User_CRM_count(income_level=income_level)
    else:
        User_CRM_count(pincode=pincode)
    return HttpResponse('success')
