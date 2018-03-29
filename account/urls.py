from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login', views.MyLoginView.as_view(), name='login'),
    path('logout', views.MyLogoutView.as_view(), name='logout'),
    # path('update/<str:pk>', views.UserUpdate.as_view(), name='update'),
    path('myaccount/update', views.MyAccountUpdate.as_view(), name='update_myaccount'),
    path('myaccount/passchange', views.PasswordChangeView.as_view(), name='passchange'),
    ]
