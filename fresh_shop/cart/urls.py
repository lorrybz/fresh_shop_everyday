from django.urls import path
from cart import views

urlpatterns = [
    # 加入购物车
    path('add_cart/',views.add_cart,name='add_cart'),
    # 购物车数量的刷新
    path('cart_num/',views.cart_num,name='cart_num'),
    path('cart/',views.cart,name='cart'),
    # 购物车计算价格
    path('cart_price/',views.cart_price,name='cart_price'),
    # 修改购物车的数量、选择状态
    path('change_cart/',views.change_cart,name='change_cart'),
    # 删除商品中的信息
    path('del_goods/',views.del_goods,name='del_goods'),
    path('del_goods/<int:id>/',views.del_goods,name='del_goods'),
    # 复选框操作
    path('is_select/',views.is_select,name='is_select'),
]

