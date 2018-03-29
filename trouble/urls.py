from django.urls import path
from . import views


urlpatterns = [
    path('', views.TroubleListView.as_view(), name='trouble_list'),
    path('<int:pk>', views.TroubleDetailView.as_view(), name='trouble_detail'),
    path('create/', views.TroubleCreateView.as_view(), name='trouble_create'),
    path('update/<int:pk>', views.TroubleUpdateView.as_view(), name='trouble_update'),
    path('delete/<int:pk>', views.TroubleDeleteView.as_view(), name='trouble_delete'),
    path('trouble_user/', views.TroubleUserListView.as_view(), name='trouble_user_list'),
    path('trouble_user/<int:pk>', views.TroubleUserDetailView.as_view(), name='trouble_user_detail'),
    path('trouble_user/create', views.TroubleUserCreateView.as_view(), name='trouble_user_create'),
    path('trouble_user/update/<int:pk>', views.TroubleUserUpdateView.as_view(), name='trouble_user_update'),
    path('trouble_user/delete/<int:pk>', views.TroubleUserDeleteView.as_view(), name='trouble_user_delete'),
    path('trouble_category/', views.TroubleCategoryListView.as_view(), name='trouble_category_list'),
    path('trouble_category/<int:pk>', views.TroubleCategoryDetailView.as_view(), name='trouble_category_detail'),
    path('trouble_category/create', views.TroubleCategoryCreateView.as_view(), name='trouble_category_create'),
    path('trouble_category/update/<int:pk>', views.TroubleCategoryUpdateView.as_view(), name='trouble_category_update'),
    path('trouble_category/delete/<int:pk>', views.TroubleCategoryDeleteView.as_view(), name='trouble_category_delete'),
    path('trouble/ajax/troubledetail/', views.get_trouble_detail_view, name='get_trouble_detail'),
    path('auto_create', views.auto_create_trouble_view, name='auto_create_trouble'),
    ]
