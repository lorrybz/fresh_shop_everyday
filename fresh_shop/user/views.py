from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from goods.models import Goods
from user.form import ResgiterForm, LoginForm, AddressForm
from user.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')

    if request.method == 'POST':
        form = ResgiterForm(request.POST)
        if form.is_valid():
            # 账号不存在与数据库，密码和确认密码一致，邮箱格式正确
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username,
                               password=password,
                               email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            errors = form.errors
            return render(request,'register.html',{'errors':errors})

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 密码相同
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return render(request,'login.html',{'errors':errors})

def logout(request):
    if request.method == 'GET':
        # 删除session中的键值对的id
        # del request.session['user_id']
        request.session.flush()
        # if request.session.get('goods'):
        #     del request.session['goods']
        return HttpResponseRedirect(reverse('goods:index'))


def user_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        activate = 'site'
        return render(request,'user_center_site.html',
                      {'user_address':user_address,'activate':activate})

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address=address,
                                       signer_name=username,
                                       signer_mobile=mobile,
                                       signer_postcode=postcode
                                       )
            return HttpResponseRedirect(reverse('user:user_site'))
        else:
            errors = form.errors
            return render(request,'user_center_site.html',
                          {'errors':errors})

def user_info(request):
    if request.method == 'GET':
        activate = 'info'
        historys = request.session.get('historys')[::-1]

        goods = []
        if len(historys) < 5:
            for id in historys:
                good = Goods.objects.filter(id=id).first()
                goods.append(good)
        else:
            for id in historys[0:5]:
                good = Goods.objects.filter(id=id).first()
                goods.append(good)
        return render(request,'user_center_info.html',
                      {'activate':activate,'goods':goods})