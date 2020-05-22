from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="ShopHome"),
    path('about/',views.about,name="AboutUs"),
    path('contact/',views.contact,name="ContactUs"),
    path('tracker/',views.tracker,name="Tracker"),
    path('search/',views.search,name="Search"),
    path('productView/<int:myid>',views.productView,name="Product View"),
    path('checkout/',views.checkout,name="Checkout"),
    path('handlerequest/',views.handlerequest,name="HandleRequest"),
    path('media1/',views.media1,name="Media1"),
    path('signUp/',views.handleSignUp,name='handleSignUp'),
    path('login/',views.handleLogin,name='handleLogin'),
    path('logout/',views.handleLogout,name='handleLogout')
]
