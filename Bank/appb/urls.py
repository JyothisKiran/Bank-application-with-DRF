from django.urls import path
from .views import GetBankDetails,BankDetailList,BankDetailsbyIFSC,BankDetailsbyNameCity,RegisterView,LoginView,UserView,LogoutView


urlpatterns = [
    path('details/<int:pk>/',GetBankDetails.as_view(),name='getbankdetails'),
    path('list/',BankDetailList.as_view(),name='banklist'),
    path('searchifsc/',BankDetailsbyIFSC.as_view(),name='searchifsc'),
    path('searchname/',BankDetailsbyNameCity.as_view(),name='searchname'),

    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('userview/',UserView.as_view(),name='userview'),
    path('logout/',LogoutView.as_view(),name='logout'),

]
