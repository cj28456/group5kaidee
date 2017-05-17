from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgres://ahtflsegcqgozm:6319391a11d35e710c39a63571b914d9ef592df788a3d3395b34d24b9b14c770@ec2-54-225-118-55.compute-1.amazonaws.com:5432/da2flrqkcgahbt?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:secret@localhost/kaidee_solution'
db=SQLAlchemy(app)

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

class Filter_type_options(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filter_type_id =  db.relationship('Filter_type',
        backref=db.backref('options', lazy='dynamic'))
    value = db.Column(db.String(100), unique=True)

    def __init__(self, filter_type_id, value):
        self.filter_type_id = filter_type_id
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
            'image_path': self.image_path,
            'description': self.description
        }
        return product_cat

class Product_sub_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    image_path = db.Column(db.Text)
    description = db.Column(db.Text, nullable=True)
    parent_category = db.relationship('Product_category',
        backref=db.backref('parent_cat', lazy='dynamic'))

    def __init__(self, name, image_path, parent_category, description=None):
        self.name = name
        self.image_path = image_path
        self.parent_category = parent_category
        self.description = description
        
    def __repr__(self):
        return  '<Product_category %r>' % self.name

    def get_product_sub_cat(self):
        product_sub_cat = {
            'id': self.id,
            'name': self.name,
            'image_path': self.image_path,
            'parent_category': self.parent_category,
            'description': self.description
        }
        return product_sub_cat

class Product_status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<Product_status %r>' % self.value

    def get_product_status(self):
        product_status = {
            'id': self.id,
            'value': self.value
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_cat_id = db.Column(db.Integer, db.ForeignKey('product_sub_category.id'))
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    product_status = db.Column(db.Integer, db.ForeignKey('product_status.id'))
    created_at = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    shipment = db.ForeignKey('filter_type_options.id')

    def __init__(self, user_id, product_cat_id, name, price, description, location, phone, shipment=None):
        self.user_id = user_id
        self.product_cat_id = product_cat_id
        self.name = name
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
            'id' = self.id,
            'user_id' = self.user_id,
            'product_cat_id' = self.product_cat_id,
            'name' = self.name,
            'price' = self.price,
            'description' = self.description,
            'location' = self.location,
            'phone' = self.phone,
            'product_status' = self.product_status,
            'shipment' = self.shipment,
            'created_at' = self.created_at,
            'last_updated' = self.last_updated,
            'deleted_at' = self.deleted_at
        }
        return product

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    rate_point = db.Column(db.Integer)

    def __init__(self, user_id, product_id, rate_point):
        self.user_id = user_id
        self.product_id = product_id
        self.rate_point

    def __repr__(self):
        return  '<Rating %r>' % self.rate_point

    def get_rate_point(self):
        rate_point = {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'rate_point': self.rate_point
        }
        return rate_point

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name

    def __repr__(self):
        return  '<Role %r>' % self.name

    def get_role(self):
        role = {
            'id': self.id,
            'name': self.name
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(150))
    avatar = db.Column(db.Text, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, username, first_name='', last_name='', phone='', email=''):
        self.username = username
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
            'role': self.role_id
        }

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
            'image_path': self.image_path,
            'created_at': self.created_at
        }

if __name__ == '__main__':
    app.run(debug=True)