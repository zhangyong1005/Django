用户表

```mysql
CREATE TABLE user(
user_id INT  NOT NULL AUTO_INCREMENT,
user_name VARCHAR(40) NOT NULL,
user_password VARCHAR(40) NOT NULL,
user_money FLOAT(20,2) DEFAULT 0,
user_power INT DEFAULT 0,
user_spend FLOAT(20,2) DEFAULT 0,
);
```

商品表

```mysql
CREATE TABLE goods(
goods_id INT  NOT NULL AUTO_INCREMENT,
goods_name VARCHAR(100) NOT NULL,
goods_price FLOAT(10,2) NOT NULL,
goods_sales INT DEFAULT 0,
goods_evaluate_number INT DEFAULT 0,
goods_info text,
goods_img  VARCHAR(500),
goods_final_grade int DEFAULT 0,
);
```

购物车表

```mysql
CREATE TABLE shoppingcar(
shoppingcar_id INT AUTO_INCREMENT,
user_id INT NOT NULL,
goods_id INT NOT NULL,
goods_type INT NOT NULL,
buy_number INT NOT NULL,
);
```

订单表

```mysql
CREATE TABLE shopped(
shopped_id INT AUTO_INCREMENT,
user_id INT NOT NULL,
goods_id INT NOT NULL,
goods_grade INT,
goods_evaluate text,
shopped_time varchar(100),
goods_evaluate_answer text,
buy_number INT NOT NULL,
goods_type INT NOT NULL,
);
```

分类

```mysql
CREATE TABLE sort(
sort_id  INT AUTO_INCREMENT,
goods_id INT NOT NULL,
goods_sort INT NOT NULL,
);
```



