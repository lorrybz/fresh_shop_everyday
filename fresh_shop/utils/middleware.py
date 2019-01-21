import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User


class TestMiddleware1(MiddlewareMixin):

    def process_request(self,request):
        # 拦截请求之前的函数
        # 1.给request.user属性赋值，赋值为当前登录系统的用户
        #对所有的请求都进行登录状态的校验


        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        path = request.path
        if path == '/':
            return None
        # 不需要做登录校验的地址
        not_need_check = ['/user/register/','/user/login/',
                          '/goods/index/','/goods/detail/.*/',
                          '/cart/.*/']
        for check_path in not_need_check:
            if re.match(check_path,path):
                return None
        # path为需要做登录校验的路由时，判断用户是否登录，没有登录则跳转到登录
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))

        # # 第二种验证方式
        # path = request.path
        # if path not in ['/user/register/','/user/login/']:
        #     try:
        #         user_id =  request.session.get('user_id')
        #         if user_id:
        #             user = User.objects.get(pk=user_id)
        #             request.user = user
        #     except Exception as e:
        #         if path in ['/goods/index/']:
        #             return None
        #         else:
        #             return HttpResponseRedirect(reverse('user:login'))

class SessionToDbMiddleware(MiddlewareMixin):
    def process_response(self,request,response):
        # 同步session中的商品信息和数据库中购物车列表
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            # 判断session中的商品是否存在于数据库中，
            # 如果存在则更新，
            # 如果不存在则创建

            # 同步数据库的数据到session
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                # 其实就是修改se_goods结构为[goods_id,num,is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id,goods_id=se_goods[0]).first()
                    if cart:
                        # 更新操作
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 在购物车中创建商品信息
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums = se_goods[1],
                                                    is_select=se_goods[2])

            # 同步数据中的session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            # 组装多个商品结构[[],[],[],[]]
            if db_carts:
                new_session_goods = [[cart.goods_id,cart.nums,cart.is_select] for cart in db_carts]
                # result = []
                # for cart in db_carts:
                #     data = [cart.goods_id,cart.nums,cart.is_select]
                #     result.append(data)
                request.session['goods'] = new_session_goods

        return response