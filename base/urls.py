from django.urls import path
from .views import product_list, product_details, sell_products
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),

    path('profile/<str:pk>/', views.userProfile, name="user-profile"),


    path('delete-message/<str:pk>', views.deleteMessage, name="deletemessage"),

    path('products/', views.product_list, name = "product_list"),
    path('product/<int:pk>/', views.product_details, name = "product_details" ),
    path('shop/', views.Shop, name = "shop")
]