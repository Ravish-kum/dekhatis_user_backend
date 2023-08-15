from celery import shared_task
from .models import Query_CRM_table, User_CRM_table, Serving_CRM_table
from .serializers import Query_CRM_Serializer, User_CRM_Serializer,Serving_CRM_Serializer
import datetime
from django.db.models import Q
from django.db.models import F
import logging
logger = logging.getLogger('my_web')
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
def query_crm(shop_id=None, item_id=None, category=None, item_cost=None, date_time=None, checkout_pincode=None, customer_id=None, theme_id= None, cancellations_customer_id=None):
    
    query_object = Query_CRM_table.objects.all()
    empty_object =[]

    if shop_id:
        local = None        
        for instance in query_object:
        
            if instance.shop_id == str(shop_id):
                local = instance
                break
            elif instance.shop_id == None:
                empty_object.append(instance)

        if local is not None:
            local.shop_count =F('shop_count') + 1
            local.save()
        
        elif len(empty_object) != 0:
            
            empty_object[0].shop_id=  shop_id
            empty_object[0].shop_count= 1
            empty_object[0].save()    
            empty_object.clear()

        else:    

            data= {'shop_id':str(shop_id), 'shop_count':1}
            serializer = Query_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in quer_Crm function (case shop_id)- error : %s',str(e) )

    elif item_id:
        local = None
        for instance in query_object:
            if instance.item_id == item_id:
                local = instance
                break
            elif instance.item_id == None:
                empty_object.append(instance)

        if local is not None:
            local.item_count = F('item_count')+1
            local.save()

        elif len(empty_object) != 0:
            empty_object[0].item_id=  item_id
            empty_object[0].item_count= 1
            empty_object[0].save()    
            empty_object.clear()

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
        local = None
        for instance in query_object:
            if instance.category == category:
                local = instance
                break
            elif instance.category == None:
                empty_object.append(instance)

        if local is not None:
            local.category_count = F('category_count')+1
            local.save()

        elif len(empty_object) != 0:
            empty_object[0].category=  category
            empty_object[0].category_count= 1
            empty_object[0].save()    
            empty_object.clear()

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
        for instance in query_object[0:12]:
        
            if  month_name(date_time) == instance.month :
                if instance.month_count == None:
                    instance.month_count =1
                    instance.save()
                    
                else:
                    instance.month_count=F('month_count') + 1
                    instance.save()
            else:
                pass
          
            if week_name(date_time) == instance.week :
                if instance.week_count == None:
                    instance.week_count =1
                    instance.save()
                    
                else:
                    instance.week_count=F('week_count') + 1
                    instance.save()
            else:
                pass
    
            if time_range(date_time) == instance.time :
                if instance.time_count == None:
                    instance.time_count =1
                    instance.save()
                    
                else:
                    instance.time_count=F('time_count') + 1
                    instance.save()
                    
            else:
                pass

    elif checkout_pincode:
        local = None
        for instance in query_object:
            if instance.checkout_pincode == checkout_pincode:
                local = instance
                break
            elif instance.checkout_pincode == None:
                empty_object.append(instance)

        if local is not None:
            local.checkout_pincode_count = F('checkout_pincode_count')+1
            local.save()

        elif len(empty_object) != 0:
            empty_object[0].checkout_pincode=  checkout_pincode
            empty_object[0].checkout_pincodeunt= 1
            empty_object[0].save()    
            empty_object.clear()

        else:
            data= {'checkout_pincode':str(checkout_pincode), 'checkout_pincode_count':1}
            serializer = Query_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in quer_Crm function (case checkout_pincode) - error : %s',str(e) )

    elif customer_id :
        local = None
        for instance in query_object:
            if instance.customer_id == customer_id:
                local = instance
                break
            elif instance.customer_id == None:
                empty_object.append(instance)

        if local is not None:
            local.customer_count = F('customer_count')+1
            local.save()

        elif len(empty_object) != 0:
            empty_object[0].customer_id=  customer_id
            empty_object[0].customer_count= 1
            empty_object[0].save()    
            empty_object.clear()

        else:
            data= {'customer_id':str(customer_id), 'customer_count':1}
            serializer = Query_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in quer_Crm function (case customer_id) - error : %s',str(e) )

    elif theme_id:
        local = None
        for instance in query_object:
            if instance.theme_id == str(theme_id):
                local = instance
                break
            elif instance.theme_id == None:
                empty_object.append(instance)

        if local is not None:
            local.theme_count = F('theme_count')+1
            local.save()

        elif len(empty_object) != 0:
            empty_object[0].theme_id=  theme_id
            empty_object[0].theme_count= 1
            empty_object[0].save()    
            empty_object.clear()

        else:
            data= {'theme_id':str(theme_id), 'theme_count':1}
            serializer = Query_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in quer_Crm function (case theme_id)- error : %s',str(e) )

    elif cancellations_customer_id:
        local = None
        for instance in query_object:
            print(cancellations_customer_id)
            if instance.cancellations_customer_id == str(cancellations_customer_id):
                local = instance
                break
            elif instance.cancellations_customer_id == None:
                empty_object.append(instance)

        if local is not None:
            local.cancellations_customer_count = F('cancellations_customer_count')+1
            local.save()

        elif len(empty_object) != 0:
            empty_object[0].cancellations_customer_id=  cancellations_customer_id
            empty_object[0].cancellations_customer_count= 1
            empty_object[0].save()    
            empty_object.clear()

        else:
            data= {'cancellations_customer_id':str(cancellations_customer_id), 'cancellations_customer_count':1}
            serializer = Query_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in quer_Crm function (case cancellations_customer_id) - error : %s',str(e) )

    
# Serving_CRM_count function is used in GettingDescription , ProductSearch (get, post), crm_cart_item_call,
#                                       Roomfilters, ThemeDiscriptionsDisplay, CustomerCreations (post)
@shared_task
def serving_CRM_count(search=None,category=None,cost=None,item_id_for_cart=None,item_id_for_desc=None,
                      checkout_view_count=None,theme_id_for_desc=None, theme_category=None):

    serving_object = Serving_CRM_table.objects.all()
    empty_object =[]
    if search:
        local = None
        for instance in serving_object:
            if instance.searches == search:
                local = instance
                break
            elif instance.searches == None:
                empty_object.append(instance)

        if local is not None:
            local.searches_count =F('searches_count') + 1
            local.save()
            
        elif len(empty_object) != 0:
            empty_object[0].searches = search
            empty_object[0].searches_count = 1
            empty_object[0].save()
            empty_object.clear()

        else:
            data= {'searches':str(search),'searches_count':1}
            serializer=  Serving_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in serving_Crm_count function (case search)- error : %s',str(e) )
            
    elif category:
        local = None
        for instance in serving_object:
            if instance.category == category :
                local = instance
                break
            elif instance.category == None:
                empty_object.append(instance)

        if local is not None:
            local.category_count =F('category_count') + 1
            local.save()
            
        elif len(empty_object) != 0:
            empty_object[0].category = category
            empty_object[0].category_count = 1
            empty_object[0].save()
            empty_object.clear()

        else:
            data= {'category':str(category),'category_count':1}
            serializer=  Serving_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in serving_Crm_count function (case category)- error : %s',str(e) )

    elif item_id_for_cart:
        local =None
        for instance in serving_object:
            if item_id_for_cart ==instance.cart_items:
                local = instance
                break
            elif instance.cart_items == None :
                empty_object.append(instance)                    
        
        if local is not None:
            local.cart_items_count =F('cart_items_count') + 1
            local.save()
        elif len(empty_object) != 0:
            empty_object[0].cart_items = item_id_for_cart
            empty_object[0].cart_items_count = 1
            empty_object[0].save()
            empty_object.clear()
            
        else:
            data= {'cart_items':str(item_id_for_cart),'cart_items_count':1}
            serializer=  Serving_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in serving_Crm_count function (case item_id_for_cart)- error : %s',str(e) )

    elif item_id_for_desc:
    
        local = None
        for instance in serving_object:
            if item_id_for_desc == instance.description_view :
                local = instance
                break
            elif instance.description_view == None:
                empty_object.append(instance)

        if local is not None:
            local.description_view_count =F('description_view_count') + 1
            local.save()
            
        elif len(empty_object) != 0:
            empty_object[0].description_view = item_id_for_desc
            empty_object[0].description_view_count = 1
            empty_object[0].save()
            empty_object.clear()

        else:
            data= {'description_view':str(item_id_for_desc),'description_view_count':1}
            serializer=  Serving_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                    logger.info('error found in serving_Crm_count function (case item_id_for_desc)- error : %s',str(e) )
    
    elif checkout_view_count:
        
            if checkout_view_count == True:
                print('in if')
                if serving_object[0].checkout_view_count == None:
                    try:
                        serving_object[0].checkout_view_count = 1
                        serving_object[0].save()
                    except Exception as e:
                        logger.info('failed to save checkout count %s',str(e))

            try:     
                if serving_object:
                    serving_object[0].checkout_view_count = F('checkout_view_count') + 1
                    try:
                        serving_object[0].save()
                    except Exception as e:
                        logger.info('failed to save checkout count %s',str(e))
                else:
                    logger.info('failed to get serving object in checkout count %s',str(e))
            except Exception as transaction_error:
                logger.info('failed to save checkout count %s',str(e))
                    
    elif cost:
        for instance in serving_object[0:21]:
            if  find_cost_range(cost) == instance.price_item_view :
                if instance.price_item_view_count == None:
                    instance.price_item_view_count =1
                    instance.save()
                    break
                else:
                    instance.price_item_view_count=F('price_item_view_count') + 1
                    instance.save()
                    break
            else:
                pass

    elif theme_id_for_desc:
        local = None
        for instance in serving_object:
            if theme_id_for_desc == instance.theme_description_view :
                local = instance
                break
            elif instance.theme_description_view == None:
                empty_object.append(instance)

        if local is not None:
            local.theme_description_view_count =F('theme_description_view_count') + 1
            local.save()
            
        elif len(empty_object) != 0:
            empty_object[0].theme_description_view = theme_id_for_desc
            empty_object[0].theme_description_view_count = 1
            empty_object[0].save()
            empty_object.clear()

        else:
            data= {'theme_description_view':str(theme_id_for_desc),'theme_description_view_count':1}
            serializer=  Serving_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in serving_Crm_count function (case theme_id_for_desc)- error : %s',str(e) )
                

    elif theme_category:
        local =None
        for instance in serving_object:
            if theme_category == instance.theme_category :
                local = instance
                break
            elif instance.theme_category == None :
                empty_object.append(instance)                    
        
        if local is not None:
            local.theme_category_count =F('theme_category_count') + 1
            local.save()
        elif len(empty_object) != 0:
            empty_object[0].theme_category = theme_category
            empty_object[0].theme_category_count = 1
            empty_object[0].save()
            empty_object.clear()
            
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
    User_object= User_CRM_table.objects.all()
    empty_object =[]

    if age:
        local =None
        for instance in User_object:
            if age == instance.age :
                local = instance
                break
            elif instance.age == None :
                empty_object.append(instance)                    
        
        if local is not None:
            local.age_count =F('age_count') + 1
            local.save()
        elif len(empty_object) != 0:
            empty_object[0].age = age
            empty_object[0].age_count = 1
            empty_object[0].save()
            empty_object.clear()
            
        else:
            data = {'age':age, 'age_count': 1}
            serializer = User_CRM_Serializer(data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                    logger.info('error found in User_Crm_count function (case age)- error : %s',str(e) )

    elif gender:
        
        for instance in User_object[0:2]:
            if gender == instance.gender:
                if instance.gender_count==None:
                    instance.gender_count= 1
                    instance.save()
                else:
                    instance.gender_count= F('gender_count')+1
                    instance.save()
        

    elif income_level:
        for instance in User_object[0:21]:
            if  find_salary_range(income_level) == instance.income_level:
                if instance.income_level_count == None:
                    instance.income_level_count =1
                    instance.save()
                    break
                else:
                    instance.income_level_count=F('income_level_count') + 1
                    instance.save()
                    break
            else:
                pass
                  
    elif pincode:
        local =None
        for instance in User_object:
            if pincode == instance.pincode :
                local = instance
                break
            elif instance.pincode == None :
                empty_object.append(instance)                    
        
        if local is not None:
            local.pincode_count =F('pincode_count') + 1
            local.save()
        elif len(empty_object) != 0:
            empty_object[0].pincode = pincode
            empty_object[0].pincode_count = 1
            empty_object[0].save()
            empty_object.clear()
            
        else:
            data= {'pincode':pincode, 'pincode_count':1}
            serializer = User_CRM_Serializer(dataa=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except Exception as e:
                logger.info('error found in User_Crm_count function (case pincode)- error : %s',str(e) )
