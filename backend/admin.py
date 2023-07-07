from django.contrib import admin
from .models import Product,Shop_table, Customer_table,Query_table,Images_table,Advertisement_table,Review_table, Cancellations_table,User, ThemeFurnituresBookings , ThemeFurniture,Dekhatis_Delivery_table,Wood_Servicing_table
from .models import My_CancellationsAdmin,My_ShopTableModelAdmin,My_Query_table_Admin, My_Product_ModelAdmin, My_UserAdmin,My_advertise_ModelAdmin,My_image_ModelAdmin,My_review_ModelAdmin, My_ThemeFurnitureAdmin, My_ThemeFurnituresBookingsAdmin,My_CustomerTableModelAdmin,My_Dekhatis_DeliveryAdmin,My_Wood_ServicingAdmin

# Register your models here.

admin.site.register(Images_table,My_image_ModelAdmin)
admin.site.register(Advertisement_table,My_advertise_ModelAdmin)
admin.site.register(Review_table,My_review_ModelAdmin)
admin.site.register(Product, My_Product_ModelAdmin)
admin.site.register(Shop_table, My_ShopTableModelAdmin)
admin.site.register(Query_table, My_Query_table_Admin)
admin.site.register(Cancellations_table,  My_CancellationsAdmin)
admin.site.register(Customer_table, My_CustomerTableModelAdmin)
admin.site.register(User, My_UserAdmin)
admin.site.register(ThemeFurniture, My_ThemeFurnitureAdmin)
admin.site.register(ThemeFurnituresBookings, My_ThemeFurnituresBookingsAdmin)
admin.site.register(Wood_Servicing_table, My_Wood_ServicingAdmin)
admin.site.register(Dekhatis_Delivery_table, My_Dekhatis_DeliveryAdmin)

