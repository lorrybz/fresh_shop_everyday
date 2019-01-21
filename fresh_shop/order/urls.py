from django.urls import path

from order import views
urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),

    path('order/',views.order,name='order'),
    # 全部订单
    path('user_order/',views.user_order,name='user_order')

]