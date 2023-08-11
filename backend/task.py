from celery import shared_task
from .models import Query_CRM_table, User_CRM_table, Serving_CRM_table
from .serializers import Query_CRM_Serializer, User_CRM_Serializer,Serving_CRM_Serializer
import datetime
from django.db.models import Q
from django.db.models import F
import logging
logger = logging.getLogger('my_web')
#==========================================================================================================================================================
#================================================================CRM control================================================================================


def find_cost_range(item_cost):
        ranges = [
            (10, 1000),(1000, 5000),(5000, 10000),(10000, 15000),(15000, 20000),(20000, 25000),(25000, 30000),(30000, 35000),(35000, 40000),(40000, 45000),
            (45000, 50000),(50000, 55000),(55000, 60000),(60000, 65000),(65000, 70000),(70000, 75000),(75000, 80000),(80000, 85000),(85000, 90000),
            (90000, 95000),(95000, 100000)
        ]

        for lower, upper in ranges:
            if lower <= item_cost < upper:
                item_cost_range =f"{lower}-{upper}"
                return item_cost_range

        return "95000-100000"

#=============================================================================================================================================================

def find_salary_range(income):
    ranges=[(100000, 200000),(200000, 300000),(300000, 400000),(400000, 500000),(500000, 600000),(600000, 700000),(700000, 800000),(800000, 900000),
            (900000, 1000000),(1000000, 2000000),(2000000, 3000000),(3000000, 4000000),(4000000, 5000000)
            ]
   
    income= int(income)

    if income <100000:
        return "100000-200000"
    for lower, upper in ranges:
        if lower <= income < upper:
            return f"{lower}-{upper}"
    else:
        return "4000000-5000000" 
        
#=================================================================================================================================================================
def month_name(date_time):
    date_string = str(date_time)
    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
    month_name = date_obj.strftime("%B")
    return month_name

#=====================================================================================================================================================================

def week_name(date_time):     
    date_string = str(date_time)
    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
    week_name = date_obj.strftime("%A")
    return week_name

#====================================================================================================================================================================

def time_range(date_time):
    date_string=str(date_time)
    hour_obj = datetime.datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S.%f")
    hour= hour_obj.strftime("%H")
    time_list =[(1,4),(4,8),(8,12),(12,16),(16,20),(20,24)]
    for lower, upper in time_list:
        if lower<= int(hour) <upper:
            time_range =f"{lower}-{upper}"
            return time_range
        else:
            time_range ="20-24"
 
 
 #============================================================================================================================================================
# query_crm function is used in checkout class
@shared_task
def query_crm(shop_id=None, item_id=None, category=None, item_cost=None, date_time=None, checkout_pincode=None, customer_id=None, theme_id= None):
    print('his')
    if shop_id:
        print('save')
        query_object = Query_CRM_table.objects.filter(shop_id= shop_id).first()
        empty_object = Query_CRM_table.objects.filter(shop_id = None).first()
        if query_object:
            print('save2')
            query_object.shop_count = F('shop_count')+1
            query_object.save()
        else:
            if empty_object:
                empty_object.shop_id=  shop_id
                empty_object.shop_count= 1
                empty_object.save()
            else:
                data= {'shop_id':str(shop_id), 'shop_count':1}
                serializer = Query_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        print('save')
                except Exception as e:
                    logger.info('error found in quer_Crm function (case shop_id)- error : %s',str(e) )
    elif item_id:
        print('save')
        query_object = Query_CRM_table.objects.filter(item_id= item_id).first()
        empty_object = Query_CRM_table.objects.filter(item_id = None).first()
        if query_object:
            query_object.item_count = F('item_count')+1
            query_object.save()
        else:
            if empty_object:
                empty_object.item_id=  item_id
                empty_object.item_count= 1
                empty_object.save()
            else:
                data= {'item_id':str(item_id), 'item_count':1}
                serializer = Query_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        print('save')
                        serializer.save()
                except Exception as e:
                    logger.info('error found in quer_Crm function (case item_id)- error : %s',str(e) )
    elif category:
        print('save')
        query_object = Query_CRM_table.objects.filter(category= category).first()
        empty_object = Query_CRM_table.objects.filter(category = None).first()
        if query_object:
            query_object.category_count = F('category_count')+1
            query_object.save()
        else:
            if empty_object:
                empty_object.category=  category
                empty_object.category_count= 1
                empty_object.save()
            else:
                data= {'category':str(category), 'category_count':1}
                serializer = Query_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        print('save')
                        serializer.save()
                except Exception as e:
                    logger.info('error found in quer_Crm function (case category)- error : %s',str(e) )
    elif item_cost:
        print('save')
        query_object = Query_CRM_table.objects.filter(item_cost=find_cost_range(item_cost)).first()
        if query_object:
            if query_object.item_cost_count == None:
                query_object.item_cost_count =1
                query_object.save()
            else:
                query_object.item_cost_count=F('item_cost_count') + 1
                query_object.save()
    
    elif date_time:
    
        query_object_month = Query_CRM_table.objects.filter(month=month_name(date_time)).first()
        
        if query_object_month:
            if query_object_month.month_count == None:
                query_object_month.month_count =1
                query_object_month.save()
                print('save')
            else:
                query_object_month.month_count=F('month_count') + 1
                query_object_month.save()
                
        query_object_week = Query_CRM_table.objects.filter(week=week_name(date_time)).first()
        if query_object_week:
            
            if query_object_week.week_count == None:
                query_object_week.week_count =1
                query_object_week.save()
            else:
                query_object_week.week_count=F('week_count') + 1
                query_object_week.save()

        query_object_time_range = Query_CRM_table.objects.filter(time=time_range(date_time)).first()
        
        if query_object_time_range:
            if query_object_time_range.time_count == None:
                query_object_time_range.time_count =1
                query_object_time_range.save()

            else:
                query_object_time_range.time_count=F('time_count') + 1
                query_object_time_range.save()
            

    elif checkout_pincode:
        query_object = Query_CRM_table.objects.filter(checkout_pincode= checkout_pincode).first()
        empty_object = Query_CRM_table.objects.filter(checkout_pincode = None).first()
        if query_object:
            query_object.checkout_pincode_count= F('checkout_pincode_count')+1
            query_object.save()
        else:
            if empty_object:
                empty_object.checkout_pincode=  checkout_pincode
                empty_object.checkout_pincode_count= 1
                empty_object.save()
            else:
                data= {'checkout_pincode':str(checkout_pincode), 'checkout_pincode_count':1}
                serializer = Query_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                    logger.info('error found in quer_Crm function (case checkout_pincode)- error : %s',str(e) )

    elif customer_id :
        query_object = Query_CRM_table.objects.filter(customer_id= customer_id).first()
        empty_object = Query_CRM_table.objects.filter(customer_id = None).first()
        if query_object:
            query_object.customer_count = F('customer_count')+1
            query_object.save()
        else:
            if empty_object:
                empty_object.customer_id=  customer_id
                empty_object.customer_count= 1
                empty_object.save()
            else:
                data= {'customer_id':str(customer_id), 'customer_count':1}
                serializer = Query_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                    logger.info('error found in quer_Crm function (case customer_id)- error : %s',str(e) )

    elif theme_id:
        query_object = Query_CRM_table.objects.filter(theme_id= theme_id).first()
        empty_object = Query_CRM_table.objects.filter(theme_id = None).first()
        if query_object:
            query_object.theme_count= F('theme_count')+1
            query_object.save()
        else:
            if empty_object:
                empty_object.theme_id=  theme_id
                empty_object.theme_count= 1
                empty_object.save()
            else:
                data= {'theme_id':str(theme_id), 'theme_count':1}
                serializer = Query_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                    logger.info('error found in quer_Crm function (case theme_id)- error : %s',str(e) )

    
# Serving_CRM_count function is used in GettingDescription , ProductSearch (get, post), crm_cart_item_call,
#                                       Roomfilters, ThemeDiscriptionsDisplay, CustomerCreations (post)
@shared_task
def serving_CRM_count(search=None,category=None,cost=None,item_id_for_cart=None,item_id_for_desc=None,
                      checkout_view_count=None,theme_id_for_desc=None, theme_category=None):

    if search:
        serving_object = Serving_CRM_table.objects.filter(searches=search).first()
        empty_object =  Serving_CRM_table.objects.filter(searches=None).first()
        if serving_object:
            serving_object.searches_count =F('searches_count') + 1
            serving_object.save()
        else:
            if empty_object:
                empty_object.searches = search
                empty_object.searches_count = 1
                empty_object.save()
            else:
                data= {'searches':str(search),'searches_count':1}
                serializer=  Serving_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                    logger.info('error found in serving_Crm_count function (case search)- error : %s',str(e) )
            
    elif category:
        serving_object = Serving_CRM_table.objects.filter(category=category).first()
        empty_object =  Serving_CRM_table.objects.filter(category=None).first()
        if serving_object:
            serving_object.category_count =F('category_count') + 1
            serving_object.save()
        else:
            if empty_object:
                empty_object.category = category
                empty_object.category_count = 1
                empty_object.save()
            else:
                data= {'category':str(category),'category_count':1}
                serializer=  Serving_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                    logger.info('error found in serving_Crm_count function (case category)- error : %s',str(e) )

    elif item_id_for_cart:
        serving_object = Serving_CRM_table.objects.filter(cart_items=item_id_for_cart).first()
        empty_object =  Serving_CRM_table.objects.filter(cart_items=None).first()
        if serving_object:
            serving_object.cart_items_count =F('cart_items_count') + 1
            serving_object.save()
        else:
            if empty_object:
                empty_object.cart_items = item_id_for_cart
                empty_object.cart_items_count = 1
                empty_object.save()
            else:
                data= {'cart_items':str(item_id_for_cart),'cart_items_count':1}
                serializer=  Serving_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                    logger.info('error found in serving_Crm_count function (case item_id_for_cart)- error : %s',str(e) )

    elif item_id_for_desc:
        serving_object = Serving_CRM_table.objects.filter(description_view=item_id_for_desc).first()
        empty_object =  Serving_CRM_table.objects.filter(description_view=None).first()
        if serving_object:
            serving_object.description_view_count =F('description_view_count') + 1
            serving_object.save()
        else:
            if empty_object:
                empty_object.description_view = item_id_for_desc
                empty_object.description_view_count = 1
                empty_object.save()
            else:
                data= {'description_view':str(item_id_for_desc),'description_view_count':1}
                serializer=  Serving_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                     logger.info('error found in serving_Crm_count function (case item_id_for_desc)- error : %s',str(e) )
    
    elif checkout_view_count:
        print('ssf')
        instance = Serving_CRM_table.objects.first()
        print(instance)
        if instance:
            if instance.checkout_view_count ==None:
                instance.checkout_view_count =1
            else:
                instance.checkout_view_count =F('checkout_view_count') + 1
                instance.save()

    elif cost:
        
        serving_object = Serving_CRM_table.objects.filter(price_item_view=find_cost_range(cost)).first()
        if serving_object:
            if serving_object.price_item_view_count == None:
                serving_object.price_item_view_count =1
                serving_object.save()
            else:
                serving_object.price_item_view_count=F('price_item_view_count') + 1
                serving_object.save()
        else:
            pass

    elif theme_id_for_desc:
        serving_object = Serving_CRM_table.objects.filter(theme_description_view=theme_id_for_desc).first()
        empty_object =  Serving_CRM_table.objects.filter(theme_description_view=None).first()
        if serving_object:
            serving_object.theme_description_view_count =F('theme_description_view_count') + 1
            serving_object.save()
        else:
            if empty_object:
                empty_object.theme_description_view = theme_id_for_desc
                empty_object.theme_description_view_count = 1
                empty_object.save()
            else:
                data= {'theme_description_view':str(theme_id_for_desc),'theme_description_view_count':1}
                serializer=  Serving_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                     logger.info('error found in serving_Crm_count function (case theme_id_for_desc)- error : %s',str(e) )

    elif theme_category:
        serving_object = Serving_CRM_table.objects.filter(theme_category=theme_category).first()
        empty_object =  Serving_CRM_table.objects.filter(theme_category=None).first()
        if serving_object:
            serving_object.theme_category_count =F('theme_category_count') + 1
            serving_object.save()
        else:
            if empty_object:
                empty_object.theme_category = theme_category
                empty_object.theme_category_count = 1
                empty_object.save()
            else:
                data= {'theme_category':str(theme_category),'theme_category_count':1}
                serializer=  Serving_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                     logger.info('error found in serving_Crm_count function (case theme_category)- error : %s',str(e) )


# User_CRM_count function is found in User_CRM_call function
@shared_task
def User_CRM_count(age=None, gender=None, income_level=None, pincode=None):
    
    if age:
        User_object= User_CRM_table.objects.filter(age=age).first()
        empty_object = User_CRM_table.objects.filter(age=None).first()
        if User_object:
            User_object.age_count = F('age_count')+1
            User_object.save()
        else:
            if empty_object:
                empty_object.age = age
                empty_object.age_count = 1
                empty_object.save()
            else:
                data = {'age':age, 'age_count': 1}
                serializer = User_CRM_Serializer(data=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                     logger.info('error found in User_Crm_count function (case age)- error : %s',str(e) )
    
    elif gender:
        print(gender)
        User_object = User_CRM_table.objects.filter(gender = gender).first()
        print(User_object)
        if User_object:
            if User_object.gender_count==None:
                User_object.gender_count= 1
                User_object.save()
            else:
                User_object.gender_count= F('gender_count')+1
                User_object.save()
        

    elif income_level:
        print(income_level)
        User_object=  User_CRM_table.objects.filter(income_level=find_salary_range(income_level)).first()
        print(find_salary_range(income_level))
        if User_object:
            if User_object.income_level_count == None:
               User_object.income_level_count= 1
               User_object.save()
            else:
                User_object.income_level_count =F('income_level_count') +1
                User_object.save()
        else:
            pass
    
    elif pincode:
        User_object = User_CRM_table.objects.filter(pincode= pincode).first()
        empty_object = User_CRM_table.objects.filter(pincode=None).first()
        if User_object:
            User_object.pincode_count=F('pincode_count')+1
            User_object.save()
        else:
            if empty_object:
                empty_object.pincode= pincode
                empty_object.pincode_count= 1
                empty_object.save()
            else:
                data= {'pincode':pincode, 'pincode_count':1}
                serializer = User_CRM_Serializer(dataa=data)
                try:
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                except Exception as e:
                    logger.info('error found in User_Crm_count function (case pincode)- error : %s',str(e) )