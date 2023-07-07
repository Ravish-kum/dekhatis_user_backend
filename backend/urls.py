from django.urls import path
from . import views
from .views import Signin, ForgotPassword, Gettingproducts,GettingDescription, ProductSearch,serve_image, Profile, Roomfilters, Cancellations,Reviews, ThemeDisplay,ThemeDiscriptionsDisplay,ThemeCancellations,Checkout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path('signin/', Signin.as_view(), name='signin'),
    path('signup/',views.signup, name='signup'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
    path('forgotpassword/', ForgotPassword.as_view(), name='forgotpassword'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path("productSearch/", ProductSearch.as_view(), name='productSearch2'),
    path("productSearch/<str:clicked_id>", ProductSearch.as_view(), name='productSearch'),
    path('gettingproducts/', Gettingproducts.as_view(), name='products'),
    path('gettingdescription/<str:myid>',GettingDescription.as_view(), name='description'),
    path('roomfilter/<str:room>',Roomfilters.as_view(),name='roomfilter'),
    path('themedisplay/',ThemeDisplay.as_view(),name='themes'),
    path('themediscriptionsdisplay/<str:id>',ThemeDiscriptionsDisplay.as_view(),name='themediscriptionsdisplay'),
    path('themecancellations/',ThemeCancellations.as_view(),name='themecancellations'),


    path('customercreations/',views.customercreations,name='customer_creations'),
    path('profile/',Profile.as_view(),name='profile'),
    path('images/<path:image_path>',serve_image,name='images'),
    path('cancellations/',Cancellations.as_view(),name='cancellations'),
    path('reviews/<str:get_id>',Reviews.as_view() ,name='reviews'),

    path('checkout/',Checkout.as_view() ,name='checkout'),
]


#rm -rf .git,sudo apt-get install git,git init,git add .,git commit -m "again stablished git",git remote add origin https://github.com/Ravish-kum/Dekhatis_api.git
#git branch -M main
#git push -u origin main



# message and error in response for success and error respectively
#400 = bad request
#401 = unauthorized
#404 = url not found
#500 = server error / something went wrong
#200 = success
#409 = item not found - by filter, get etc. 
