import time
from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.form import Form_register,Form_login,Add_good
from app.function import *
from django.core.paginator import Paginator



def check(func):
    '''
    保持登录装饰器，未登跳往登录界面
    '''

    def zyc(request):
        check = request.COOKIES.get('book_cookie')
        if check:
            return func(request)
        else:
            return redirect('login')

    return zyc


def index(request):
    '''
    首页，未登录则没有为你推荐、练习客服
    '''
    all_goods = goods_show()
    user_name = request.COOKIES.get('book_cookie')
    r=con_redis()
    if user_name != '':
        key = 'history_%s' % user_name
        history_li = r.lrange(key, 0, 19)
        goods_li = []
        for i in history_li:
            x = find_sort_from_id(i)
            if x == None:
                continue
            goods_li.extend(x)
        list1 = [goods_li.count(i) for i in range(1, 7)]
        sorts = list1.index(max(list1)) + 1
        data = book_from_sort(sorts)
        list2 = list()
        for k in data:
            list2.append([k[0], one_good_img(k[0])])
    else:
        list2 = ''
    users = all_goods
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 21)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    return render(request, 'index.html', {'user_name': user_name, 'page': page, 'li': list2})


def search(request):
    '''
    搜索商品
    '''
    name = request.COOKIES.get('book_cookie')
    word = request.POST.get('search')
    if word != '':
        all_goods = search_goods(word)
        if all_goods == () or all_goods == None:
            all_goods = ''
            response = 1
        else:
            response = 2
    else:
        all_goods = ()
        response = 0
    return render(request, 'search.html', {'goods': all_goods, 'user_name': name, 'response': response})


@check
def goods_info(request):
    '''
    商品详情页：添加购物车，查看商品评价
    '''
    if request.method == 'GET':
        goods_id = request.GET.get('id')
        final_grade(goods_id)
        user_name = request.COOKIES.get('book_cookie')
        data = one_good(goods_id)
        looktime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        r=con_redis()
        r.set(name='%s_%s' % (user_name, goods_id), value=looktime)
        key = 'history_%s' % user_name
        r.lrem(key, 0, goods_id)
        r.lpush(key, goods_id)
        r.ltrim(key, 0, 19)
        infos = data[0][5].split('\n')
        return render(request, 'goods_info.html', context={'user_name': user_name, 'infos': infos, 'key': data[0]})
    else:
        goods_id = request.GET.get('id')
        final_grade(goods_id)
        user_name = request.COOKIES.get('book_cookie')
        user_id = find_user_id(user_name)
        data = one_good(goods_id)
        infos = data[0][5].split('\n')
        buy_number = request.POST.get('buy_number')
        good_type = request.POST.get('good_type')
        if buy_number != None and good_type != None:
            response = '加入购物车成功'
            good_into_car(user_id, goods_id, good_type, buy_number)
        else:
            response = ''
        return render(request, 'goods_info.html', context={'user_name': user_name, 'infos': infos, 'key': data[0],
                                                           'response': response})


def login(request):
    '''
    登录系统
    '''
    if request.method == 'GET':
        form = Form_login()
        return render(request, 'login.html', {'form': form})
    else:
        form = Form_login(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('pass_word')
            if re_username(username):
                return render(request, 'login.html', context={'key': '用户名不存在，请注册', 'form': form})
            if true_passwd(username, password):
                response = redirect('index')
                response.set_cookie('book_cookie', username, max_age=60 * 60 * 24 * 10)
                return response
            else:
                return render(request, 'login.html', context={'key': '用户名或密码错误', 'form': form})


def register(request):
    '''
    注册系统，已存在用户名不可注册
    '''
    if request.method == 'GET':
        form = Form_register()
        return render(request, 'register.html', {'form': form})
    else:
        form = Form_register(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user_name')
            password1 = form.cleaned_data.get('pass_word1')
            password2 = form.cleaned_data.get('pass_word2')
            if password1 != password2:
                return render(request, 'register.html', context={'key': '两次密码不一样', 'form': form})
            if not re_username(username):
                return render(request, 'register.html', context={'key': '用户名已存在', 'form': form})
            insert_into(username, password1)
            response = redirect('index')
            response.set_cookie('book_cookie', username, max_age=60 * 60 * 24 * 10)
            return response


@check
def person(request):
    '''
    个人中心
    管理员多显示管理后台接口
    '''
    username = request.COOKIES.get('book_cookie')
    userpower = user_power(username)
    usermoney = user_money(username)
    return render(request, 'person.html', context={'name': username, 'power': userpower, 'money': usermoney})


def nologin(request):
    '''
    注销函数
    '''
    response = redirect('login')
    response.set_cookie('book_cookie', '')
    return response


def check_root(func):
    '''
    检验是否是管理员
    '''

    def zyc(request):
        name = request.COOKIES.get('book_cookie')
        power = user_power(name)
        if power > 1:
            return func(request)
        else:
            return HttpResponse('没有权限')

    return zyc


def check_super_root(func):
    '''
    检验超管权限
    '''

    def zyc(request):
        name = request.COOKIES.get('book_cookie')
        power = user_power(name)
        if power == 3:
            return func(request)
        else:
            return HttpResponse('快滚，不是超级管理还敢进来')

    return zyc


@check_super_root
def super_root(request):
    '''
    超级管理员后台
    '''
    data = goods_show()
    sum = 0
    for i in data:
        sum += i[1] * i[3]
    dic1 = dict()
    for k in range(1, 7):
        all_money = 0
        data = all_book_from_sort(k)
        for j in data:
            x = money_from_id(j)
            all_money += x[0] * x[1]
        dic1['money_%s' % k] = '%.2f' % all_money
    return render(request, 'super_admin.html', {'sum': '%.2f' % sum, 'type': dic1})


@check_super_root
def super_root_user(request):
    '''
    超级管理员后台管理用户，根据收到参数来进行判断展示页面内容
    '''
    if request.method == 'GET':
        id = request.GET.get('user')
        p1 = request.GET.get('p1')
        if p1 == '1':
            data = user_show_super_spend()
            return render(request, 'super_admin_user.html', {'user': data})
        elif p1 == '2':
            data = user_show_super_power()
            return render(request, 'super_admin_user.html', {'user': data})
        if id == None or id == '':
            data = user_show_super()
            return render(request, 'super_admin_user.html', {'user': data})
        else:
            data = one_user(id)
            return render(request, 'super_admin_user.html', context={'user': data, 'key': 1})
    else:
        id = request.GET.get('user')
        data = one_user(id)
        user_name = request.POST.get('user_name')
        pass_word = request.POST.get('pass_word')
        power = request.POST.get('power')
        if user_name == '':
            if pass_word == '':
                if power == None:
                    return render(request, 'super_admin_user.html',
                                  context={'user': data, 'key': 1, 'resqult': '不改别给我搞事'})
                else:
                    super_change_user(data[0][1], data[0][2], power, id)
                    data = one_user(id)
                    return render(request, 'super_admin_user.html',
                                  context={'user': data, 'key': 1, 'resqult': '权限修改成功'})
            else:
                if power == None:
                    super_change_user(data[0][1], pass_word, data[0][5], id)
                    data = one_user(id)
                    return render(request, 'super_admin_user.html',
                                  context={'user': data, 'key': 1, 'resqult': '密码修改成功'})
                else:
                    super_change_user(data[0][1], pass_word, power, id)
                    data = one_user(id)
                    return render(request, 'super_admin_user.html',
                                  context={'user': data, 'key': 1, 'resqult': '密码和权限修改成功'})
        else:
            if pass_word == '':
                if power == None:
                    if not re_username(user_name):
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名不可以重复'})
                    else:
                        super_change_user(user_name, data[0][2], data[0][5], id)
                        data = one_user(id)
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名修改成功'})
                else:
                    if not re_username(user_name):
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名不可以重复'})
                    else:
                        super_change_user(user_name, data[0][2], power, id)
                        data = one_user(id)
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名和权限修改成功'})
            else:
                if power == None:
                    if not re_username(user_name):
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名不可以重复'})
                    else:
                        super_change_user(user_name, pass_word, data[0][5], id)
                        data = one_user(id)
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名和密码修改成功'})
                else:
                    if not re_username(user_name):
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名不可以重复'})
                    else:
                        super_change_user(user_name, pass_word, power, id)
                        data = one_user(id)
                        return render(request, 'super_admin_user.html',
                                      context={'user': data, 'key': 1, 'resqult': '用户名、密码和权限修改成功'})


@check_super_root
def super_root_good(request):
    '''
    超级管理员后台管理商品，根据收到参数来进行判断展示页面内容
    '''
    if request.method == 'GET':
        id = request.GET.get('good')
        p1 = request.GET.get('p1')
        if id == None or id == '':
            if p1 == '1':
                data = goods_show_by_sales()
            elif p1 == '2':
                data = goods_show_by_price()
            else:
                data = goods_show()
            return render(request, 'super_admin_good.html', {'good': data})
        else:
            data = one_good(id)
            return render(request, 'super_admin_good.html', context={'good': data, 'key': 1})
    else:
        good_id = request.GET.get('good')
        data = one_good(good_id)
        good_name = request.POST.get('good_name')
        good_price = request.POST.get('good_price')
        good_info = request.POST.get('good_info')
        choice = request.POST.get('delete')
        if choice == '1':
            delete_good(good_id)
            return render(request, 'super_admin_good.html', context={'good': data, 'key': 1, 'response': '下架成功'})
        else:
            if good_name == '' and good_price == '':
                if good_info == data[0][5]:
                    return render(request, 'super_admin_good.html',
                                  context={'good': data, 'key': 1, 'response': '不修改就别提交'})
                else:
                    change_good_info(good_id, good_info)
                    data = one_good(good_id)
                    return render(request, 'super_admin_good.html',
                                  context={'good': data, 'key': 1, 'response': '修改成功'})
            elif good_name == '':
                change_good_info_price(good_id, good_info, good_price)
                data = one_good(good_id)
                return render(request, 'super_admin_good.html',
                              context={'good': data, 'key': 1, 'response': '修改成功'})
            else:
                change_good(good_id, good_name, good_info, good_price)
                data = one_good(good_id)
                return render(request, 'super_admin_good.html',
                              context={'good': data, 'key': 1, 'response': '修改成功'})


@check
def money(request):
    '''
    用户充值页面
    '''
    if request.method == 'GET':
        username = request.COOKIES.get('book_cookie')
        usermoney = user_money(username)
        return render(request, 'money.html', {'name': username, 'money': usermoney})
    else:
        username = request.COOKIES.get('book_cookie')
        usermoney = user_money(username)
        add_money = request.POST.get('add_money')
        if '.' in add_money:
            return render(request, 'money.html', context={'name': username, 'money': usermoney,
                                                          'key': '请填写整数及正数'})
        elif not add_money.isdigit():
            return render(request, 'money.html', context={'name': username, 'money': usermoney,
                                                          'key': '请填写整数及正数'})
        add_money = float(add_money)
        money = usermoney + add_money
        change_money(username, money)
        newmoney = user_money(username)
        return render(request, 'money.html', {'name': username, 'money': newmoney, 'key': '充值成功'})


@check_root
def root(request):
    '''
    普通管理员后台
    '''
    data = goods_show()
    sum = 0
    for i in data:
        sum += i[1] * i[3]
    dic1 = dict()
    for k in range(1, 7):
        all_money = 0
        data = all_book_from_sort(k)
        for j in data:
            x = money_from_id(j)
            all_money += x[0] * x[1]
        dic1['money_%s' % k] = '%.2f' % all_money
    return render(request, 'super_admin.html', {'sum': '%.2f' % sum, 'type': dic1})


@check_root
def root_user(request):
    '''
    普通管理员后台管理用户，根据收到参数来进行判断展示页面内容
    '''
    id = request.GET.get('user')
    p1 = request.GET.get('p1')
    if p1 == '1':
        data = user_show_root_spend()
        return render(request, 'super_admin_user.html', {'user': data})
    elif p1 == '2':
        data = user_show_root_power()
        return render(request, 'super_admin_user.html', {'user': data})
    if id == None or id == '':
        data = user_show_root()
        return render(request, 'super_admin_user.html', {'user': data})
    else:
        return HttpResponse('你没有权限修改用户，去找超级管理员')


@check_root
def root_good(request):
    '''
    超级管理员后台管理商品，根据收到参数来进行判断展示页面内容
    '''
    if request.method == 'GET':
        id = request.GET.get('good')
        p1 = request.GET.get('p1')
        if id == None or id == '':
            if p1 == '1':
                data = goods_show_by_sales()
            elif p1 == '2':
                data = goods_show_by_price()
            else:
                data = goods_show()
            return render(request, 'super_admin_good.html', {'good': data})
        else:
            data = one_good(id)
            return render(request, 'super_admin_good.html', context={'good': data, 'key': 1})
    else:
        good_id = request.GET.get('good')
        data = one_good(good_id)
        good_name = request.POST.get('good_name')
        good_price = request.POST.get('good_price')
        good_info = request.POST.get('good_info')
        choice = request.POST.get('delete')
        if choice == '1':
            delete_good(good_id)
            return render(request, 'super_admin_good.html', context={'good': data, 'key': 1, 'response': '下架成功'})
        else:
            if good_name == '' and good_price == '':
                if good_info == data[0][5]:
                    return render(request, 'super_admin_good.html',
                                  context={'good': data, 'key': 1, 'response': '不修改就别提交'})
                else:
                    change_good_info(good_id, good_info)
                    data = one_good(good_id)
                    return render(request, 'super_admin_good.html',
                                  context={'good': data, 'key': 1, 'response': '修改成功'})
            elif good_name == '':
                change_good_info_price(good_id, good_info, good_price)
                data = one_good(good_id)
                return render(request, 'super_admin_good.html',
                              context={'good': data, 'key': 1, 'response': '修改成功'})
            else:
                change_good(good_id, good_name, good_info, good_price)
                data = one_good(good_id)
                return render(request, 'super_admin_good.html',
                              context={'good': data, 'key': 1, 'response': '修改成功'})


@check
def change(request):
    '''
    用户修改密码
    '''
    if request.method == 'GET':
        name = request.COOKIES.get('book_cookie')
        return render(request, 'change_person.html', {'name': name})
    else:
        name = request.COOKIES.get('book_cookie')
        old_password = request.POST.get('old_pass_word')
        password1 = request.POST.get('pass_word1')
        password2 = request.POST.get('pass_word2')
        if old_password == '':
            return render(request, 'change_person.html', {'name': name, 'key': '请填写原密码'})
        elif password1 == '' or password2 == '':
            return render(request, 'change_person.html', {'name': name, 'key': '请填写新密码'})
        elif password1 != password2:
            return render(request, 'change_person.html', {'name': name, 'key': '两次密码不一致'})
        elif not true_passwd(name, old_password):
            return render(request, 'change_person.html', {'name': name, 'key': '原密码不正确'})
        elif password2 == old_password:
            return render(request, 'change_person.html', {'name': name, 'key': '新旧密码一致'})
        else:
            change_passwd(name, password1)
            return render(request, 'change_person.html', {'name': name, 'key': '修改成功'})


@check
def shoppingcar(request):
    '''
    购物车，普通用户以上打98折
    '''
    if request.method == 'GET':
        user_name = request.COOKIES.get('book_cookie')
        user_id = find_user_id(user_name)
        data = find_car(user_id)
        sum = 0
        li = list()
        for i in data:
            k = one_good(i[2])
            sum += i[4] * k[0][2]
            li.append([i[0], k[0][1], k[0][2], k[0][6], i[3], i[4], i[4] * k[0][2]])
        power = user_power(user_name)
        if power > 0:
            sum1 = sum * 0.98
        else:
            sum1 = ''
        if li == []:
            choice = 0
        else:
            choice = 1
        return render(request, 'shoppingcar.html',
                      context={'key': li, 'user_name': user_name, 'sum': "%.2f" % sum, 'sum1': sum1, 'key2': choice})
    else:
        pay = request.POST.get('ral')
        user_name = request.COOKIES.get('book_cookie')
        user_id = find_user_id(user_name)
        data = find_car(user_id)
        if pay == '1':
            del_car(user_id)
            return render(request, 'shoppingcar.html',
                          context={'user_name': user_name, 'key2': 0})
        sum = 0
        power = user_power(user_name)

        money = user_money(user_name)
        for i in data:
            k = one_good(i[2])
            sum += i[4] * k[0][2]
        if power > 0:
            sum1 = sum * 0.98
            if money > sum1:
                new_money = money - sum1
                old_spend = user_spend(user_name)
                new_spend = old_spend + sum
                change_spend(user_name, new_spend)
                change_money(user_name, new_money)
                data = find_car(user_id)
                for i in data:
                    shoppedtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    buy_car(user_id, i[2], shoppedtime, i[3], i[4])
                    goods_sales(i[2], i[4])
                    print(i[2], i[4])
                    del_car(user_id)
                return render(request, 'shoppingcar.html',
                              context={'user_name': user_name, 'key2': 2, 'key3': '付款成功'})
            else:
                return render(request, 'shoppingcar.html',
                              context={'user_name': user_name, 'key2': 2, 'key3': '余额不足，请去个人中心充值'})
        if money > sum:
            new_money = money - sum
            old_spend = user_spend(user_name)
            new_spend = old_spend + sum
            change_spend(user_name, new_spend)
            change_money(user_name, new_money)
            data = find_car(user_id)
            for i in data:
                shoppedtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                buy_car(user_id, i[2], shoppedtime, i[3], i[4])
                goods_sales(i[2], i[4])
                print(i[2], i[4])
                del_car(user_id)
            return render(request, 'shoppingcar.html',
                          context={'user_name': user_name, 'key2': 2, 'key3': '付款成功'})
        else:
            return render(request, 'shoppingcar.html',
                          context={'user_name': user_name, 'key2': 2, 'key3': '余额不足，请去个人中心充值'})


@check
def look_history(request):
    '''
    浏览记录，redis取
    '''
    user_name = request.COOKIES.get('book_cookie')
    r=con_redis()
    key = 'history_%s' % user_name
    history_li = r.lrange(key, 0, 19)
    goods_li = []
    for i in history_li:
        goods_li.append((one_good_name(i), i, r.get('%s_%s' % (user_name, i))))

    if goods_li == []:
        return render(request, 'look_history.html', {'key': goods_li, 'user_name': user_name, 'response': '你没有浏览记录'})
    else:
        return render(request, 'look_history.html', {'key': goods_li, 'user_name': user_name})


def sort(request):
    '''
    商品分类
    '''
    goods_sort = request.GET.get('p1')
    goods_ids = find_sort(goods_sort)
    tuple1 = tuple()
    for goods_id in goods_ids:
        tuple1 += (sort_goods(goods_id))
    name = request.COOKIES.get('book_cookie')
    users = tuple1
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 21)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    return render(request, 'sort.html', {'user_name': name, 'page': page, 'sort': goods_sort})


@check
def car_order(request):
    '''
    修改购物车内信息
    '''
    if request.method == 'GET':
        order_number = request.GET.get("number")
        data = find_car_order(order_number)
        goods = one_good(data[0][2])
        infos = goods[0][5].split('\n')
        username = request.COOKIES.get('book_cookie')
        return render(request, 'car_order.html', {'user_name': username, 'infos': infos,
                                                  'key': goods[0], 'key2': data[0]})
    else:
        order_number = request.GET.get("number")
        new_type = int(request.POST.get('good_type'))
        new_buy = int(request.POST.get('buy_number'))
        no_shopping = request.POST.get('dfc')
        if no_shopping == '3':
            delete_one_shoppingcar(order_number)
            return redirect('shoppingcar')
        data = find_car_order(order_number)
        if new_buy != data[0][4] or new_type != data[0][3]:
            response = '修改成功'
            new_car(data[0][0], new_type, new_buy)
            data = find_car_order(order_number)
        else:
            response = '不改就回去付款吧'
        goods = one_good(data[0][2])
        infos = goods[0][5].split('\n')
        username = request.COOKIES.get('book_cookie')
        return render(request, 'car_order.html', {'user_name': username, 'infos': infos,
                                                  'key': goods[0], 'key2': data[0], 'response': response})


@check
def shopped(request):
    '''
    购买记录
    '''
    user_name = request.COOKIES.get('book_cookie')
    user_id = find_user_id(user_name)
    data = sel_shoped(user_id)
    tuple1 = tuple()
    for i in data:
        if i[8] == 0:
            a = '精美书皮'
        elif i[8] == 1:
            a = '精美书签'
        else:
            a = '精美挂件'
        tuple1 += ((one_good_name(i[2]), i[3], i[4], i[5], i[6], i[7], a, i[0]),)
    return render(request, 'shopped_history.html', {'key': tuple1, 'user_name': user_name})


@check
def goods_evaluate(request):
    '''
    对已经购买的商品进行评分评价
    '''
    user_name = request.COOKIES.get('book_cookie')
    shopped_id = request.GET.get('id')
    if request.method == 'GET':
        data = good_evaluate(shopped_id)
        tuple1 = tuple()
        i = data[0]
        if i[8] == 0:
            a = '精美书皮'
        elif i[8] == 1:
            a = '精美书签'
        else:
            a = '精美挂件'
        tuple1 += (one_good_name(i[2]), i[3], i[4], i[5], i[6], i[7], a, one_good_img(i[2]))
        return render(request, 'good_evaluate.html', {'user_name': user_name, 'key': tuple1})
    else:
        new_grade = request.POST.get('grade')
        new_evaluate = request.POST.get('user_evaluate')
        if new_grade == '空值' or new_grade == '':
            if new_evaluate == '':
                data = good_evaluate(shopped_id)
                tuple1 = tuple()
                i = data[0]
                if i[8] == 0:
                    a = '精美书皮'
                elif i[8] == 1:
                    a = '精美书签'
                else:
                    a = '精美挂件'
                tuple1 += (one_good_name(i[2]), i[3], i[4], i[5], i[6], i[7], a, one_good_img(i[2]))
                return render(request, 'good_evaluate.html',
                              {'user_name': user_name, 'key': tuple1, 'response': '不修改就不修改吧'})
            else:
                new_eva(shopped_id, new_evaluate)
            data = good_evaluate(shopped_id)
            tuple1 = tuple()
            i = data[0]
            if i[8] == 0:
                a = '精美书皮'
            elif i[8] == 1:
                a = '精美书签'
            else:
                a = '精美挂件'
            tuple1 += (one_good_name(i[2]), i[3], i[4], i[5], i[6], i[7], a, one_good_img(i[2]))
            return render(request, 'good_evaluate.html', {'user_name': user_name, 'key': tuple1, 'response': '修改成功'})
        elif new_grade.isdigit() and 0 < int(new_grade) < 6:
            if new_evaluate == '':
                new_gr(shopped_id, new_grade)
            else:
                new_gr_eva(shopped_id, new_grade, new_evaluate)
            data = good_evaluate(shopped_id)
            tuple1 = tuple()
            i = data[0]
            if i[8] == 0:
                a = '精美书皮'
            elif i[8] == 1:
                a = '精美书签'
            else:
                a = '精美挂件'
            tuple1 += (one_good_name(i[2]), i[3], i[4], i[5], i[6], i[7], a, one_good_img(i[2]))
            return render(request, 'good_evaluate.html', {'user_name': user_name, 'key': tuple1, 'response': '修改成功'})
        else:
            data = good_evaluate(shopped_id)
            tuple1 = tuple()
            i = data[0]
            if i[8] == 0:
                a = '精美书皮'
            elif i[8] == 1:
                a = '精美书签'
            else:
                a = '精美挂件'
            tuple1 += (one_good_name(i[2]), i[3], i[4], i[5], i[6], i[7], a, one_good_img(i[2]))
            return render(request, 'good_evaluate.html',
                          {'user_name': user_name, 'key': tuple1, 'response': '请给1-5的整数分'})


@check
def goods_talk(request):
    '''
    一个商品的具体评价，管理员多一个修改商家回复按钮
    '''
    goods_id = request.GET.get('p1')
    data = user_good_talk(goods_id)
    user_name = request.COOKIES.get('book_cookie')
    power = user_power(user_name)
    tuple1 = tuple()
    for i in data:
        tuple1 += ((one_user(i[0])[0][1], i[1], i[2], i[3], i[4]),)
    return render(request, 'goods_talk.html',
                  {'key': tuple1, 'user_name': user_name, 'good_id': goods_id, 'user_power': power})


@check_root
def change_evaluate_answer(request):
    '''
    修改商家回复
    '''
    shopped_id = request.GET.get('id')
    if request.method == 'GET':
        data = good_evaluate(shopped_id)
        return render(request, 'change_evaulate_answer.html', {'data': data[0]})
    else:
        an = request.POST.get('p1')
        if an == '':
            data = good_evaluate(shopped_id)
            return render(request, 'change_evaulate_answer.html', {'data': data[0], 'key': '不改别捣乱'})
        else:
            up_answer(shopped_id, an)
            data = good_evaluate(shopped_id)
            return render(request, 'change_evaulate_answer.html', {'data': data[0], 'key': '修改成功'})


@check_root
def add_good(request):
    '''
    添加商品
    '''
    if request.method == 'GET':
        data = Add_good()
        return render(request, 'add_good.html', {'data': data})
    else:
        data = Add_good(request.POST)
        if data.is_valid():
            good_name = data.cleaned_data.get('good_name')
            good_price = data.cleaned_data.get('good_price')
            good_info = data.cleaned_data.get('good_info')
            good_img = data.cleaned_data.get('good_img')
            root_add_good(good_name, good_price, good_info, good_img)
            return render(request, 'add_good.html', {'data': data, 'key': '添加成功'})


@check
def chat(request):
    '''
    一个聊天室
    '''
    user_name = request.COOKIES.get('book_cookie')
    chat_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return render(request, 'room.html', {'user_name': user_name, 'chat_time': chat_time})
