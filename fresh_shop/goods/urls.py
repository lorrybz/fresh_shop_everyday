from django.urls import path
from  goods import views
urlpatterns = [
    # 首页
    path('index/',views.index,name='index'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('list/<int:id>/',views.list,name='list'),
    path('search/',views.search,name='search')
]