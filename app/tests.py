import pymysql
from bs4 import BeautifulSoup
import requests
conn=pymysql.connect(host='127.0.0.1', port=3306,
                               user='root', passwd='root',
                               db='bookstore', charset='utf8')
cursor = conn.cursor()
url = 'https://list.tmall.com/search_product.htm?q=%BD%CC%BF%C6%CA%E9&type=p&spm=a220m.1000858.a2227oh.d100&from=.list.pc_1_searchbutton'
response = requests.get(url)  # 解析网页
soup = BeautifulSoup(response.text, 'lxml')  # .text将解析到的网页可读
storenames = soup.select('#J_ItemList > div > div > p.productTitle > a')  # 选择出商店的信息
prices = soup.select('#J_ItemList > div > div > p.productPrice > em')  # 选择出价格的信息
sales = soup.select('#J_ItemList > div > div > p.productStatus > span > em')  # 选择出销售额的信息
imgs = soup.select('#J_ItemList > div > div > div.productImg-wrap > a > img')
a_hrefs=soup.select('#J_ItemList > div > div >  p.productTitle > a')
for storename, price, sale, img,a_href in zip(storenames, prices, sales, imgs,a_hrefs):
    storename = storename.get_text().strip()  # 用get_text()方法筛选出标签中的文本信息，由于筛选结果有换行符\n所以用strip()将换行符去掉
    price = price.get_text()[1:]
    sale = sale.get_text()
    if '万笔'in sale:
        sale=int(float(sale[0:-2])*10000)
    else:
        sale=int(sale[0:-1])
    if img.get('src') == None:
        img='http:' +img.get('data-ks-lazyload')
    else:
        img = 'http:' + img.get('src')
    print(img)
    print('商品名:%-40s\n价格:%-40s\n销售额:%s' % (storename, price, sale))
    a_href = 'http:' + a_href.get('href')
    url1 = a_href
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.text, 'lxml')
    infos = soup1.select('#J_AttrUL > li')
    all_info=''
    for info in infos:
        info = info.get_text()
        all_info+=info+'\n'
    print(all_info)
    cursor.execute("insert into goods(goods_name,goods_price,goods_sales,goods_evaluate_number,goods_info,goods_img,goods_final_grade)values('%s','%s','%s','%s','%s','%s',5) " % (storename,price,sale,sale,all_info,img))
    print('------------------------------------------------------------------------------------')
conn.commit()
cursor.close()
conn.close()