import pymysql
import redis
def con_redis():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r

def con_mysql():
    return pymysql.connect(host='127.0.0.1', port=3306,
                           user='root', passwd='root',
                           db='bookstore', charset='utf8')


def insert_into(UserName, PassWord):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("insert into user(user_name,user_password)values('%s','%s') " % (UserName, PassWord))
    conn.commit()
    cursor.close()
    conn.close()


def re_username(UserName):
    '''
    param : UserName
    return:
    用户名不存在输出正确
    用户名存在则输出错误
    '''
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_name from user where user_name='%s'" % UserName)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(data) == 0:
        return True
    else:
        return False


def true_passwd(UserName, PassWord):
    '''
    :param UserName:
    :param PassWord:
    :return: 密码正确则正确
    '''
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_name,user_password from user where user_name='%s'" % UserName)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if data[0][1] == PassWord:
        return True
    else:
        return False


def change_passwd(name, password):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update user set user_password='%s' where user_name='%s'" % (password, name))
    conn.commit()
    cursor.close()
    conn.close()


def super_change_user(name, passwd, power, id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update user set user_name='%s',user_password='%s',user_power='%s' where user_id='%s'" % (
    name, passwd, power, id))
    conn.commit()
    cursor.close()
    conn.close()


def user_money(UserName):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_money from user where user_name='%s'" % UserName)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]


def change_money(name, money):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update user set user_money='%s' where user_name='%s'" % (money, name))
    conn.commit()
    cursor.close()
    conn.close()


def user_spend(UserName):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_spend from user where user_name='%s'" % UserName)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]


def change_spend(name, money):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update user set user_spend='%s' where user_name='%s'" % (money, name))
    conn.commit()
    cursor.close()
    conn.close()


def user_power(UserName):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_power from user where user_name='%s'" % UserName)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]


def goods_show():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_name,goods_price,goods_img,goods_sales,goods_id from goods ")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def goods_show_by_sales():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_name,goods_price,goods_img,goods_sales,goods_id from goods ORDER BY goods_sales DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def goods_show_by_price():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_name,goods_price,goods_img,goods_sales,goods_id from goods ORDER BY goods_price DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def user_show_super():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_id,user_name,user_spend,user_power from user where user_power<3")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def user_show_root():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_id,user_name,user_spend,user_power from user where user_power<2")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def user_show_super_spend():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "select user_id,user_name,user_spend,user_power from user where user_power<3 ORDER BY user_spend DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def user_show_root_spend():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "select user_id,user_name,user_spend,user_power from user where user_power<2 ORDER BY user_spend DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def user_show_super_power():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "select user_id,user_name,user_spend,user_power from user where user_power<3 ORDER BY user_power DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def user_show_root_power():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "select user_id,user_name,user_spend,user_power from user where user_power<2 ORDER BY user_power DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def one_user(id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "select user_id,user_name,user_password,user_money,user_spend,user_power from user where user_id='%s'" % id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def search_goods(name):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_name,goods_price,goods_img,goods_sales,"
                   "goods_id from goods where goods_name like '%%%s%%'" % name)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def one_good(id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select * from goods where goods_id='%s'" % id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def one_good_name(id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_name from goods where goods_id='%s'" % id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]


def one_good_img(id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_img from goods where goods_id='%s'" % id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]


def goods_sales(id, buy_number):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_sales from goods where goods_id='%s'" % id)
    data = cursor.fetchall()
    new_sale = data[0][0] + buy_number
    cursor.execute("update goods set goods_sales='%s' where goods_id=%s" % (new_sale, id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_good(good_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("delete from goods where goods_id=%s" % good_id)
    conn.commit()
    cursor.close()
    conn.close()


def delete_one_shoppingcar(shoppingcar_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("delete from shoppingcar where shoppingcar_id=%s" % shoppingcar_id)
    conn.commit()
    cursor.close()
    conn.close()


def change_good_info(good_id, good_info):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update goods  set goods_info='%s' where goods_id=%s" % (good_info, good_id))
    conn.commit()
    cursor.close()
    conn.close()


def change_good_info_price(good_id, good_info, good_price):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "update goods  set goods_info='%s',goods_price='%s' where goods_id=%s" % (good_info, good_price, good_id))
    conn.commit()
    cursor.close()
    conn.close()


def change_good(good_id, good_name, good_info, good_price):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update goods  set goods_name='%s',goods_info='%s',goods_price='%s' where goods_id=%s" % (
    good_name, good_info, good_price, good_id))
    conn.commit()
    cursor.close()
    conn.close()


def good_into_car(user_id, goods_id, goods_type, buy_number):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("insert into shoppingcar(user_id,goods_id,goods_type,buy_number)values('%s','%s','%s','%s') " % (
    user_id, goods_id, goods_type, buy_number))
    conn.commit()
    cursor.close()
    conn.close()


def find_user_id(user_name):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_id from user where user_name='%s'" % user_name)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][0]


def find_car(user_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select * from shoppingcar where user_id='%s'" % user_id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def sel_shoped(user_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select * from shopped where user_id='%s'ORDER BY shopped_id DESC LIMIT 15" % user_id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def del_car(user_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("delete from shoppingcar where user_id=%s" % user_id)
    conn.commit()
    cursor.close()
    conn.close()


def buy_car(user_id, goods_id, time, goods_type, buy_number):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "insert into shopped(user_id,goods_id,shopped_time,goods_type,buy_number) values('%s','%s','%s','%s','%s') " % (
        user_id, goods_id, time, goods_type, buy_number))
    conn.commit()
    cursor.close()
    conn.close()


# 195,435
def hanshu():
    conn = con_mysql()
    cursor = conn.cursor()
    for i in range(195, 435):
        if i == 213:
            continue
        cursor.execute(
            "INSERT INTO shopped(user_id,goods_id,goods_grade,goods_evaluate,shopped_time,goods_evaluate_answer,buy_number,goods_type)VALUES(1,'%s',5,'是本好书','2019-09-06 10:48:00','亲，感谢你的支持',1,2)" % i)
        conn.commit()
    cursor.close()
    conn.close()


def find_sort(sort_):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_id from sort where goods_sort='%s'" % sort_)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def find_sort_from_id(id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_sort from sort where goods_id='%s'" % id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(data) > 0:
        s_li = []
        for i in data:
            s_li.append(i[0])
        return s_li


def sort_goods(goods_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "select goods_name,goods_price,goods_img,goods_sales,goods_id from goods where goods_id=%s" % goods_id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def find_car_order(id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select * from shoppingcar where shoppingcar_id=%s" % id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def new_car(id, type, number):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "update shoppingcar set goods_type='%s',buy_number='%s' where shoppingcar_id='%s'" % (type, number, id))
    conn.commit()
    cursor.close()
    conn.close()


def good_evaluate(shopped_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select * from shopped where shopped_id=%s" % shopped_id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def new_eva(shopped_id, eva):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update shopped set shopped_evaluate='%s' where shopped_id=%s" % (eva, shopped_id))
    conn.commit()
    cursor.close()
    conn.close()


def new_gr(shopped_id, gra):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update shopped set goods_grade='%s' where shopped_id=%s" % (gra, shopped_id))
    conn.commit()
    cursor.close()
    conn.close()


def new_gr_eva(shopped_id, gra, eva):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "update shopped set goods_grade='%s',goods_evaluate='%s' where shopped_id=%s" % (gra, eva, shopped_id))
    conn.commit()
    cursor.close()
    conn.close()


def final_grade(goods_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_grade from shopped where goods_id='%s'" % goods_id)
    data = cursor.fetchall()
    evaluate_number = len(data)
    if evaluate_number != 0:
        sum = 0
        for i in data:
            if i[0] == None:
                evaluate_number -= 1
            else:
                sum += i[0]
        grade = (float(sum) / evaluate_number)
        cursor.execute("update goods set goods_final_grade='%s',goods_evaluate_number='%s'" % (grade, evaluate_number))
        conn.commit()
        cursor.close()
        conn.close()


def user_good_talk(goods_id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute(
        "select user_id,goods_grade,goods_evaluate,goods_evaluate_answer,shopped_id from shopped where goods_id='%s'" % goods_id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def all_book_from_sort(sort):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_id from sort where goods_sort='%s'" % sort)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def money_from_id(id):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_price,goods_sales from goods where goods_id='%s'" % id)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0]


def book_from_sort(sort):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select goods_id from sort where goods_sort='%s' ORDER BY sort_id DESC LIMIT 3" % sort)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def root_add_good(good_name, good_price, good_info, good_img):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("insert into goods(goods_name,goods_price,goods_info,goods_img)values('%s','%s','%s','%s')"
                   % (good_name, good_price, good_info, good_img))
    conn.commit()
    cursor.close()
    conn.close()


def up_answer(shopped_id, an):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update shopped set goods_evaluate_answer='%s' where shopped_id=%s" % (an, shopped_id))
    conn.commit()
    cursor.close()
    conn.close()


def all_user_name():
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select user_name from user")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data
