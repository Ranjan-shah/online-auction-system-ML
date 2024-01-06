from django.urls import path
from .import views
from myapp.views import electronics
from myapp.views import vehicle
from myapp.views import realstate
from myapp.views import sports
from myapp.views import jewelry



urlpatterns=[
    path('',views.product_View.as_view(),name='index'),
    path('mybidding:<int:pk>',views.mybiddingView.as_view(),name='mybidding'),
    path('profile',views.myprofile.as_view(),name='profile'),
    path('update-profile',views.get_updated,name='get_update'),
    path('my-bidding',views.get_details.as_view(),name='get_details'),
    path('listing',views.listing_page.as_view(),name='listing_page'),
    path('electronics',electronics,name='electronics_page'),
    path('vehicle',vehicle,name='vehicle_page'),
    path('real state',realstate,name='realstate_page'),
    path('sports',sports,name='sports_page'),
    path('jewelry',jewelry,name='jewelry_page'),
    path('contact',views.contact_page.as_view(),name='contact_page'),
    path('carpredict/', views.carpredict, name='carpredict'),
    path('carpredicts/', views.carpredicts, name='carpredicts'),
    path('housepredict/',views.housepredict_page, name='housepredict_page'),
    path('housepredict/result/',views.resultp,name='housepredict_page'),
     path('bikepredict/', views.bikepredict, name='bikepredict'),
    path('bikepredicts/', views.bikepredicts, name='bikepredicts'),
    
  
]

