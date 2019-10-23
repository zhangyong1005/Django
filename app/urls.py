from django.urls import path

from app.views import *

urlpatterns = [
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('index/',index,name='index'),
    path('search/',search,name='search'),
    path('goods_info/',goods_info,name='one_goods_info'),
    path('person/',person,name='person'),
    path('admin/',root,name='admin'),
    path('admin/good/',root_good,name='admin_good'),
    path('admin/user/',root_user,name='admin_user'),
    path('admin/add_good/',add_good,name='root_add_good'),
    path('superadmin/',super_root,name='superadmin'),
    path('superadmin/user/',super_root_user,name='superadmin_user'),
    path('superadmin/good/',super_root_good,name='superadmin_good'),
    path('superadmin/add_good/',add_good,name='super_add_good'),
    path('nologin/',nologin,name='nologin'),
    path('money/',money,name='money'),
    path('change/',change,name='change'),
    path('shoppingcar/',shoppingcar,name='shoppingcar'),
    path('look_history/',look_history,name='look_history'),
    path('sort/',sort,name='sort'),
    path('order/',car_order,name="car_order"),
    path('shopped/',shopped,name='shopped'),
    path('evaluate/',goods_evaluate,name='good_evaluate'),
    path('goods_talk/',goods_talk,name='goods_talk'),
    path('answer/',change_evaluate_answer,name='answer'),
    path('chat/', chat, name='chat'),
]
