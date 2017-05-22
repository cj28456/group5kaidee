from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from datetime import datetime
from flask import request
from sqlalchemy import update, or_
import hashlib
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgres://zpknyaqnuexyam:51aeefba47ecb62f184afdf3c4a6845ebd38eb82cfcf868636490ee13fa2d4cc@ec2-54-243-107-66.compute-1.amazonaws.com:5432/dfc0cnd8ugng68?sslmode=require'
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:หำแพำะ@localhost/kaidee_resolution'

db=SQLAlchemy(app)

# Base url for image_path in API
# site_url = 'http://localhost:5000'
site_url = 'https://group5-kaidee-resolution.herokuapp.com'
image_url = 'http://162.243.54.156/'

# conn = psycopg2.connect("dbname='kaidee_resolution' user='postgres' password='หำแพำะ' host='localhost' port='5432'")
conn = psycopg2.connect("dbname='dfc0cnd8ugng68' user='zpknyaqnuexyam' password='51aeefba47ecb62f184afdf3c4a6845ebd38eb82cfcf868636490ee13fa2d4cc' host='ec2-54-243-107-66.compute-1.amazonaws.com' port='5432'")
cur = conn.cursor()

# filter_type table schema
class Filter_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return  '<Filter_type %r>' % self.name
        
    def get_filter_type(self):
        filter_type = {
            'id': self.id,
            'name': self.name
        }
        return filter_type

# filter_type_options table schema
class Filter_type_options(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filter_type_id = db.Column(db.Integer, db.ForeignKey('filter_type.id'))
    filter_type =  db.relationship('Filter_type',
        backref=db.backref('options', lazy='dynamic'))
    value = db.Column(db.String(100), unique=True)

    def __init__(self, filter_type, value):
        self.filter_type = filter_type
        self.value = value
        
    def __repr__(self):
        return  '<Filter_type_option %r>' % self.value

    def get_filter_type_option(self):
        filter_type_option = {
            'id': self.id,
            'filter_type_id': self.filter_type_id,
            'value': self.value
        }
        return filter_type_option


# product_category table schema
class Product_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    image_path = db.Column(db.Text)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, image_path, description=None):
        self.name = name
        self.image_path = image_path
        self.description = description
        
    def __repr__(self):
        return  '<Product_category %r>' % self.name

    def get_product_cat(self):
        product_cat = {
            'id': self.id,
            'name': self.name,
            'image_path': site_url + self.image_path,
            'description': self.description
        }
        return product_cat

# product_sub_category table schema
class Product_sub_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    image_path = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    product_category = db.relationship('Product_category',
        backref=db.backref('parent', lazy='dynamic'))
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, image_path, product_category, description=None):
        self.name = name
        self.image_path = image_path
        self.product_category = product_category
        self.description = description
        
    def __repr__(self):
        return  '<Product_category %r>' % self.name

    def get_product_sub_cat(self):
        product_sub_cat = {
            'id': self.id,
            'name': self.name,
            'image_path': site_url + self.image_path,
            'parent_category_id': self.parent_category_id,
            'description': self.description
        }
        return product_sub_cat

# product_status table (store product's status)
# class Product_status(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Integer)

#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return '<Product_status %r>' % self.value

#     def get_product_status(self):
#         product_status = {
#             'id': self.id,
#             'value': self.value
#         }
#         return product_status


# product table schema
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User',
        backref=db.backref('user', lazy='joined'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    product_category = db.relationship('Product_category',
        backref=db.backref('category', lazy='dynamic'))
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))

    product_sub_category = db.relationship('Product_sub_category',
        backref=db.backref('sub_category', lazy='dynamic'))
    product_sub_category_id = db.Column(db.Integer, db.ForeignKey('product_sub_category.id'))
    name = db.Column(db.String(100))
    image_path = db.Column(db.Text)
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    # product_status = db.relationship('Product_status',
    #     backref=db.backref('status', lazy='dynamic'))
    # product_status_id = db.Column(db.Integer, db.ForeignKey('product_status.id'))
    product_status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    shipment = db.Column(db.Text)
    boost = db.Column(db.Integer, default=0)

    def __init__(self, user, product_category, product_sub_category, name, image_path, price, description, location, phone, shipment=None, boost=0):
        self.user = user
        self.product_category = product_category
        self.product_sub_category = product_sub_category
        self.name = name
        self.image_path = image_path
        self.price = price
        self.description = description
        self.location = location
        self.phone = phone
        self.shipment = shipment
        self.product_status = 1
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return  '<Product %r>' % self.name

    def get_product(self):
        product={
            'id': self.id,
            'user_id': self.user_id,
            'product_cat_id': self.product_category_id,
            'product_subcat_id': self.product_sub_category_id,
            'name': self.name,
            'image_path': image_url + self.image_path,
            'price': self.price,
            'description': self.description,
            'location': self.location,
            'phone': self.phone,
            'product_status': self.product_status,
            'shipment': self.shipment,
            'rating': self.cal_rating(),
            'boost': self.boost,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            'deleted_at': self.deleted_at
        }
        return product

    def cal_rating(self):
        product_num = 0
        sum_point = 0
        avg_rating = 3
        # get user id
        cur.execute('SELECT user_id FROM product WHERE id = %s;', [self.id])
        result = cur.fetchall()
        user_id = result[0][0]

        cur.execute('SELECT count(product_id) FROM rating WHERE user_id = %s;', [user_id])
        if cur.rowcount != 0:
            result = cur.fetchall()
            product_num = result[0][0]
               
        cur.execute('SELECT sum(rate_point) FROM rating WHERE user_id = %s;', [user_id])
        if cur.rowcount != 0:
            result = cur.fetchall()
            sum_point = result[0][0]

        if product_num !=0 and sum_point !=0:
            avg_rating = sum_point/product_num
        
        return round(avg_rating, 0)

# rating table schema
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User',
        backref=db.backref('users', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.relationship('Product',
        backref=db.backref('products', lazy='dynamic'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    rate_point = db.Column(db.Integer)
    who_id = db.Column(db.Integer)

    def __init__(self, user, product, who_id, rate_point):
        self.user = user
        self.who_id = who_id
        self.product = product
        self.rate_point = rate_point

    def __repr__(self):
        return  '<Rating on product %r>' % self.product

    def get_rate_point(self):
        rate_point = {
            # 'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'rate_point': self.rate_point,
            'who_id': self.who_id
        }
        return rate_point


# role table schema
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return  '<Role %r>' % self.name

    def get_role(self):
        role = {
            'id': self.id,
            'name': self.name
        }
        return role


# user table schema
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.Text)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    avatar = db.Column(db.Text, nullable=True)
    role = db.relationship('Role',
        backref=db.backref('role', lazy='dynamic'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, username, password, first_name, last_name, phone, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.role_id = 2

    def __repr__(self):
        return  '<User %r>' % self.username

    def get_user(self):
        user = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'avatar': self.avatar,
            'role': self.role_id,
            'rating' : self.cal_rating()
        }
        return user

    def cal_rating(self):
        product_num = 0
        sum_point = 0
        avg_rating = 3
        cur.execute('SELECT count(product_id) FROM rating WHERE user_id = %s;', [self.id])
        if cur.rowcount != 0:
            result = cur.fetchall()
            product_num = result[0][0]
               
        cur.execute('SELECT sum(rate_point) FROM rating WHERE user_id = %s;', [self.id])
        if cur.rowcount != 0:
            result = cur.fetchall()
            sum_point = result[0][0]

        if product_num !=0 and sum_point !=0:
            avg_rating = sum_point/product_num

        return round(avg_rating, 0)

    def rating_check(self):
        user = {
            'id': self.id,
            'rating' : self.cal_rating()
        }
        return user

# advertisment table schema
class Advertisment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    link = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    def __init__(self, name, image_path, link=''):
        self.name = name
        self.image_path = image_path
        self.link = link
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return  '<Advertisment %r>' % self.name

    def get_ads(self):
        ads = {
            'id': self.id,
            'name': self.name,
            'link': self.link,
            'image_path': site_url + self.image_path,
            'created_at': self.created_at
        }
        return ads


################# API route #################
# get all main product category
@app.route('/get_product_cat', methods=['GET'])
def get_product_cat():
    product_cats = Product_category.query.all()
    results = []
    for product_cat in product_cats:
        results.append(product_cat.get_product_cat())
    return jsonify({'product_cat': results})


# get product sub-category
@app.route('/get_product_sub_cat/<parent_category_id>', methods=['GET'])
def get_product_sub_cat(parent_category_id):
    product_sub_cats = Product_sub_category.query.filter_by(parent_category_id=parent_category_id)
    results = []
    for product_sub_cat in product_sub_cats:
        results.append(product_sub_cat.get_product_sub_cat())

    # products = Product.query.filter_by(product_category_id=parent_category_id)
    products = Product.query.filter( (Product.product_category_id == parent_category_id) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.id).all()
    results_products = []
    for product in products:
        results_products.append(product.get_product())

    return jsonify({'product_sub_cat': results, 'product_in_cat': results_products})


# filter product as per user choices in select main product category
@app.route('/get_product_sub_cat/<parent_category_id>', methods=['POST'])
def get_product_sub_cat_filter(parent_category_id):
    results = []
    search_str = ''
    min_price = 0
    max_price = 999999999
    main_filter = 'price'
    order_by = 'asc'
    shipping = ''
    shipping_choices = []

    #check each args existed. if not use the default value that define above
    if 'search_text' in request.args:
        search_str = request.args['search_text']
        
    if 'min_price' in request.args and request.args['min_price'] != '':
        min_price = request.args['min_price']

    if 'max_price' in request.args and request.args['max_price'] != '':
        max_price = request.args['max_price']

    if 'main_filter' in request.args and request.args['main_filter'] != '':
        main_filter = request.args['main_filter']

    if 'order_by' in request.args and request.args['order_by'] != '':
        order_by = request.args['order_by']

    if 'shipping' in request.args and request.args['shipping'] != '':
        shipping = request.args['shipping']
        shipping_choices = shipping.split(',') # split each shipping choices

    # create sqlalchemy objects to search on product shipment column
    conditions = []
    for shipping_choice in shipping_choices:
        conditions.append(or_( Product.shipment.ilike("%"+shipping_choice+",%"), Product.shipment.ilike("%,"+shipping_choice), Product.shipment.ilike(shipping_choice) ))

    if main_filter=='price':
        if order_by=='desc':
            products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_category_id == parent_category_id ) & (Product.price.between(int(min_price), int(max_price))) | (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price.desc()).all()
        if order_by!='desc':
            products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_category_id == parent_category_id ) & (Product.price.between(int(min_price), int(max_price))) | (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price).all()
        # set json result
        for product in products:
            results.append(product.get_product())
    else:
        # get all user and calculate averange rating
        rating_list = {}
        users = User.query.all()
        for user in users:
            tmp = user.get_user()
            rating_list[tmp['id']] = tmp['rating']
        
        if order_by=='desc':
            for key, value in sorted(rating_list.items(), key=lambda t: t[1]): # sort rating_list
                products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_category_id == parent_category_id ) & (Product.price.between(int(min_price), int(max_price))) & (Product.user_id==key) & (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price.desc()).all()
                for product in products:
                    results.append(product.get_product())

            for key, value in sorted(rating_list.items(), key=lambda t: t[1]): # sort rating_list
                products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_category_id == parent_category_id ) & (Product.price.between(int(min_price), int(max_price))) & (Product.user_id==key) & (Product.boost!=1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price.desc()).all()
                for product in products:
                    results.append(product.get_product())
                    

        if order_by!='desc':
            for key, value in sorted(rating_list.items(), key=lambda t: t[1]): # sort rating_list
                products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_category_id == parent_category_id ) & (Product.price.between(int(min_price), int(max_price))) & (Product.user_id==key) & (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price).all()
                for product in products:
                    results.append(product.get_product())

            for key, value in sorted(rating_list.items(), key=lambda t: t[1]): # sort rating_list
                products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_category_id == parent_category_id ) & (Product.price.between(int(min_price), int(max_price))) & (Product.user_id==key) & (Product.boost!=1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price).all()
                for product in products:
                    results.append(product.get_product())

    return jsonify({'product_in_cat': results})


# get all filter list available
@app.route('/get_filter', methods=['GET'])
def get_filter_type():
    filter_types = Filter_type.query.all()
    results = []
    for filter_type in filter_types:
        results.append(filter_type.get_filter_type())
    return jsonify({'filter_type': results})


# get filter optin value if the filter have value fixed in the system
@app.route('/get_filter/<filter_type_id>', methods=['GET'])
def get_filter_type_option(filter_type_id):
    filter_type_options = Filter_type_options.query.filter_by(filter_type_id=filter_type_id)
    results = []
    for filter_type_option in filter_type_options:
        results.append(filter_type_option.get_filter_type_option())
    return jsonify({'filter_type_options': results})


#get product in product sub-category
@app.route('/get_product_in_subcat/<product_sub_category_id>', methods=['GET'])
def get_product_in_subcat(product_sub_category_id):
    products = Product.query.filter( (Product.product_sub_category_id == product_sub_category_id) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.id).all()
    results = []
    for product in products:
        results.append(product.get_product())
    return jsonify({'product_in_subcat': results})


## filter product as per user choices only in this sub-category
@app.route('/get_product_in_subcat/<product_sub_category_id>', methods=['POST'])
def get_product_in_subcat_filter(product_sub_category_id):
    results = []
    search_str = ''
    min_price = 0
    max_price = 999999999
    main_filter = 'price'
    order_by = 'asc'
    shipping = ''
    shipping_choices = []

    #check each args existed. if not use the default value that define above
    if 'search_text' in request.args:
        search_str = request.args['search_text']

    if 'min_price' in request.args and request.args['min_price'] != '':
        min_price = request.args['min_price']

    if 'max_price' in request.args and request.args['max_price'] != '':
        max_price = request.args['max_price']

    if 'main_filter' in request.args and request.args['main_filter'] != '':
        main_filter = request.args['main_filter']

    if 'order_by' in request.args and request.args['order_by'] != '':
        order_by = request.args['order_by']

    if 'shipping' in request.args and request.args['shipping'] != '':
        shipping = request.args['shipping']
        shipping_choices = shipping.split(',') # split each shipping choices

    # create sqlalchemy objects to search on product shipment column
    conditions = []
    for shipping_choice in shipping_choices:
        conditions.append(or_( Product.shipment.ilike("%"+shipping_choice+",%"), Product.shipment.ilike("%,"+shipping_choice), Product.shipment.ilike(shipping_choice) ))

    if main_filter=='price':
        if order_by=='desc':
            products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_sub_category_id == int(product_sub_category_id)) & (Product.price.between(int(min_price), int(max_price))) | (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price.desc()).all()
        if order_by!='desc':
            products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_sub_category_id == int(product_sub_category_id)) & (Product.price.between(int(min_price), int(max_price))) | (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price).all()
        # set json result
        for product in products:
            results.append(product.get_product())
    else:
        # get all user and calculate averange rating
        rating_list = {}
        users = User.query.all()
        for user in users:
            tmp = user.get_user()
            rating_list[tmp['id']] = tmp['rating']
        
        if order_by=='desc':
            for key, value in sorted(rating_list.items(), key=lambda t: t[1]): # sort rating_list
                products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_sub_category_id == int(product_sub_category_id)) & (Product.price.between(int(min_price), int(max_price))) & (Product.user_id==key) | (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price.desc()).all()
                for product in products:
                    results.append(product.get_product())
        if order_by!='desc':
            for key, value in sorted(rating_list.items(), key=lambda t: t[1]): # sort rating_list
                products = Product.query.filter( ((or_(*conditions)) & (Product.name.ilike("%"+search_str+"%")) & (Product.product_sub_category_id == int(product_sub_category_id)) & (Product.price.between(int(min_price), int(max_price))) & (Product.user_id==key) | (Product.boost==1) ) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.price).all()
                for product in products:
                    results.append(product.get_product())

    return jsonify({'product_in_subcat': results})

# get product information
@app.route('/get_product/<id>', methods=['GET'])
def get_product_info(id):
    products = Product.query.filter( (Product.id==id) & (Product.deleted_at == None) ).all()
    results = []
    for product in products:
        results.append(product.get_product())
    return jsonify({'product': results})


# get user information
@app.route('/get_user/<id>', methods=['GET'])
def get_user(id):
    users = User.query.filter_by(id=id)
    results = []
    for user in users:
        results.append(user.get_user())
    return jsonify(results)

# get user's products
@app.route('/get_my_post/<id>', methods=['GET'])
def get_my_post(id):
    products = Product.query.filter( (Product.user_id==id) & (Product.deleted_at == None) ).order_by(Product.boost.desc()).order_by(Product.id).all()
    results = []
    for product in products: 
        results.append(product.get_product())
    return jsonify(results)

# user register
@app.route('/register', methods=['POST'])
def user_register():
    status = ''
    hashed_password = ''
    message = 'Not correct informations to register'

    if not request.json or not 'username' in request.json or not 'password' in request.json or not 'first_name' in request.json or not 'last_name' in request.json or not 'phone' in request.json or not 'email' in request.json:
        status = 'error'
        message = 'Not correct informations to register'
    elif request.json['username'] == '' or request.json['password'] == '' or request.json['first_name'] == '' or request.json['last_name'] == '' or request.json['phone'] =='' or request.json['email'] == '':
        status = 'error'
        message = 'Some fields are empty value'
    elif request.json['username'] != '' and request.json['password'] !='' and request.json['first_name'] !='' and request.json['last_name'] != '' and request.json['phone'] !='' and request.json['email'] !='':
        check = User.query.filter( (User.username == request.json['username']) & (User.email == request.json['email']) ).all()
        if not check:
            # not store raw password, use hash md-5
            password = request.json['password']
            hashed_password = hashlib.md5(password.encode('utf8')).hexdigest()
            # Init User obj with data
            new_acc = User(request.json['username'], hashed_password, request.json['first_name'], request.json['last_name'], request.json['phone'], request.json['email'])
            db.session.add(new_acc)
            db.session.commit() # insert new user to database
            status = 'ok'
            message = 'Your registeration is success'
        else:
            status = 'error'
            message = 'Username or Email was use be other user'

    results = {'status': status, 'message': message}
    return jsonify(results)
    
# user login
@app.route('/login', methods=['POST'])
def user_login():
    results = []
    status = ''
    message = ''
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        status = 'error'
        message = 'Missing parameters'
    elif request.json['username']=='' or request.json['password']=='':
        status = 'error'
        message = 'Missing username or password'
    else:
        # check if there is an account registered with username and hash password
        password = request.json['password']
        hashed_password = hashlib.md5(password.encode('utf8')).hexdigest()
        users = User.query.filter( (User.username==request.json['username']) & (User.password==hashed_password) ).all()
        # users = User.query.filter( (User.username==usr) & (User.password==hash_pwd) ).all()
        if not users:
            status = 'error'
            message = 'Username or Password is incorrect'
        else:
            status = 'ok'
            message = 'Login success'
            for user in users:
                status = 'ok'
                message = user.get_user()

    results = {'status': status, 'message': message}
    return jsonify(results)

# add product (self, user, product_category, product_sub_category, name, image_path, price, description, location, phone, shipment)
@app.route('/add_product', methods=['POST'])
def add_product():
    import datetime
    results = []
    status = ''
    message = ''
    if not request.json or not 'user_id' in request.json or not 'product_category_id' in request.json or not 'product_sub_category_id' in request.json or not 'name' in request.json or not 'image_path' in request.json or not 'price' in request.json or not 'description' in request.json or not 'location' in request.json or not 'phone' in request.json or not 'shipment' in request.json:
        status = 'error'
        message = 'You didn\'t complete the correct information'
    elif request.json['user_id'] == '' or request.json['product_category_id'] == '' or request.json['product_sub_category_id'] == '' or request.json['name'] == '' or request.json['image_path'] == '' or request.json['price'] == '' or request.json['description'] == '' or request.json['location'] == '' or request.json['phone'] == '' or request.json['shipment'] == '':
        status = 'error'
        message = 'Some values are missing'
    else:
        products_info = (request.json['user_id'], request.json['product_category_id'], request.json['product_sub_category_id'], request.json['name'], request.json['image_path'], int(request.json['price']), request.json['description'], request.json['location'], request.json['phone'], 1, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), request.json['shipment'], 0)
        cur.execute("INSERT INTO product (user_id, product_category_id, product_sub_category_id, name, image_path, price, description, location, phone, product_status, created_at, shipment, boost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", products_info)
        conn.commit()
        status = 'ok'
        message = 'Your product informations is added'
    
    results = {'status': status, 'message': message}
    return jsonify(results)

# set boost
@app.route('/set_boost', methods=['POST'])
def set_boost():
    results = []
    status = ''
    message = ''
    if not request.json or 'product_id' not in request.json or request.json['product_id']=='' :
        status = 'error'
        message = 'Can\'t found this product'
    else:
        cur.execute("SELECT boost FROM product WHERE id=%s;", [request.json['product_id']])
        result = cur.fetchall()
        boost = result[0][0]
        if boost==0:
            cur.execute("UPDATE product SET boost=%s WHERE id=%s;", (1, request.json['product_id']))
            conn.commit()
            message = 'Boost was set'
        else:
            cur.execute("UPDATE product SET boost=%s WHERE id=%s;", (0, request.json['product_id']))
            conn.commit()
            message = 'Boost was unset'
        status = 'ok'
    results = {'status': status, 'message': message}
    return jsonify(results)

# get boost
# @app.route('/get_boost_list', methods=['GET'])
# def get_boost_list():
#     results =[]
#     status = ''
#     products = Product.query.filter( (Product.boost==1) & (Product.deleted_at == None) ).all()
#     if not products:
#         status = 'error'
#     else:
#         status = 'ok'
#         for product in products:
#             results.append(product.get_product())
#     return jsonify({'status': status, 'boost_products': results})

# rate user
@app.route('/rate', methods = ['POST'])
def rate_user():
    results = []
    status = ''
    message = ''
    if not request.json or 'user_id' not in request.json or not 'product_id' in request.json or not 'rate' in request.json or not 'who_is' in request.json:
        status = 'error'
        message = 'Your parameters are missing'
    elif request.json['user_id'] == '' or request.json['product_id'] == '' or request.json['rate'] == '' or request.json['who_is'] == '':
        status = 'error'
        message = 'Some values are missing'
    else:
        # check can't rate your own product
        if request.json['user_id'] != request.json['who_is']:
            rating_info = (int(request.json['user_id']), int(request.json['product_id']), int(request.json['rate']), int(request.json['who_is']))
            cur.execute("INSERT INTO rating (user_id, product_id, rate_point, who_id) VALUES (%s, %s, %s, %s)", rating_info)
            conn.commit()
            status = 'ok'
            message = 'Your rating was submit'
        else:
            status = 'error'
            message = 'Your can\'t rate your self !'

    results = {'status': status, 'message': message}
    return jsonify(results)

# delete product
@app.route('/delete_product', methods=['POST'])
def delete_product():
    results = []
    status = ''
    message = ''
    if not request.json or not 'product_id' in request.json or request.json['product_id']=='':
        status = 'error'
        message = 'Your request is not correct'
    else:
        check_id = Product.query.filter_by(id = int(request.json['product_id']))
        if check_id:
            delete_product = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()), int(request.json['product_id']))
            cur.execute("UPDATE product SET deleted_at=%s WHERE id=%s;", delete_product)
            conn.commit()
            status = 'ok'
            message = 'Product was deleted'
        else:
            status = 'error'
            message = 'This product was already deleted'
        
    results = {'status': status, 'message': message}
    return jsonify(results)
    
# filter all product
@app.route('/search_filters', methods=['POST'])
def get_product_filter_by():
    results = []
    search_str = ''
    min_price = 0
    max_price = 999999999
    order_by = 'asc'
    shipping = ''
    shipping_choices = []

    #check each args existed. if not use the default value that define above
    if 'search_text' in request.args:
        search_str = request.args['search_text']

    if 'min_price' in request.args and request.args['min_price'] != '':
        min_price = request.args['min_price']

    if 'max_price' in request.args and request.args['max_price'] != '':
        max_price = request.args['max_price']

    if 'order_by' in request.args and request.args['order_by'] != '':
        order_by = request.args['order_by']

    if 'shipping' in request.args and request.args['shipping'] != '':
        shipping = request.args['shipping']
        shipping_choices = shipping.split(',') # split each shipping choices

    # create sqlalchemy objects to search on product shipment column
    conditions = []
    for shipping_choice in shipping_choices:
        conditions.append(or_( Product.shipment.ilike("%"+shipping_choice+",%"), Product.shipment.ilike("%,"+shipping_choice), Product.shipment.ilike(shipping_choice) ))
        
    if order_by=='desc':
        products = Product.query.filter((or_(*conditions)) & (Product.price.between(min_price, max_price)) & (Product.deleted_at == None)).order_by(Product.price.desc()).all()

    if order_by!='desc':
        products = Product.query.filter((or_(*conditions)) & (Product.price.between(min_price, max_price)) & (Product.deleted_at == None) ).all()

    for product in products:
        results.append(product.get_product())
    return jsonify({'filter_products': results})

if __name__ == '__main__':
    app.run(debug=True)