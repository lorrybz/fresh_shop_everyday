from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from fresh_shop.settings import OEDER_NUMBER
from goods.models import GoodsCategory, Goods


def index(request):
    if request.method == 'GET':
        # 如果访问首页，返回渲染的首页index.html页面
        # 思路组装结果的对象object：包含分类，该分类的前四个商品信息
        # 方式一：objects==> [goodscategory objects,[good objects],[good objects]，[good objects]，[good objects]]
        # 方式二：{'category_name':[good objects],[good objects],[good objects]，[good objects]}
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods=category.goods_set.all()[0:4]
            data = [category,goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request,'index.html',
                      {'result':result,'category_type':category_type})

def detail(request,id):
    if request.method == 'GET':
        historys = request.session.get('historys',[])
        # 返回详情页面解析的商品信息
        if len(historys) == 0:
            historys.append(id)
        else:
            for i in historys[:]:
                if int(i) == id:
                    historys.remove(i)
                    historys.append(id)
                    break
            else:
                historys.append(id)
        good = Goods.objects.filter(id=id).first()
        good1 = Goods.objects.all()[0:2]
        request.session['historys'] = historys
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request,'detail.html',{'good':good,
                                             'good1':good1,
                                             'category_type':category_type,})


def list(request,id):
    if request.method == 'GET':
        goods = Goods.objects.filter(category_id=id)
        # page = int(request.GET.get('page', 1))
        # pg = Paginator(goods, OEDER_NUMBER)
        # goods = pg.page(page)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request,'list.html',{'goods':goods,'id':id,'category_type':category_type})


def search(request):
    if request.method == 'GET':
        key_words = request.GET.get('key_words')
        filter_goods = Goods.objects.filter(name__contains=key_words).all()
        return render(request, 'list1.html',{'goods':filter_goods})



