from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_brand = Namespace('Brand', description='Brand Operations')

brand_form = ns_brand.model('Brand Details', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'company_name' : fields.String(required=True, description='Company Name'),
    'email' : fields.String(required=True, description='Email'),
    'password' : fields.String(required=True, description='Password')
})


brand_edit_form = ns_brand.model('Brand Details Update', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'phone': fields.String(required=True, description='Phone'),
    'position': fields.String(required=True, description='Position'),
    'company_name': fields.String(required=True, description='Company Name'),
    'url': fields.String(required=True, description='URL'),
    'country': fields.String(required=True, description='Country'),
    'no_of_employees': fields.String(required=True, description='No Of Employees'),
    'city': fields.String(required=True, description='City'),
    'monthly_budget': fields.String(required=True, description='Monthly Budget'),
    'business_sector': fields.String(required=True, description='Business Sector')
})

@ns_brand.route('/register')
class Brand(Resource):
    @ns_brand.expect(brand_form)
    def post(self):
        '''Registers Brand Details'''
        form_data = request.get_json()
        password_sha = sha256_crypt.encrypt(str(form_data.get('password')))
        pass_dict = {'password':password_sha}
        role = {'role':'Admin'}
        form_data.update(pass_dict)
        form_data.update(role)
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        company_name = form_data.get('company_name')
        email = form_data.get('email')
        password_sha = form_data.get('password')
        role = form_data.get('role')
        columns = ['first_name', 'last_name', 'email_id', 'company_name', 'password', 'role']
        data = [first_name, last_name, email, company_name, password_sha, role]
        result=0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='users_brands',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': result},201
        except: return {'response': result},500

@ns_brand.route('/')
class Brand(Resource):
    def get(self):
        '''List of all Brands'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id','first_name','last_name','company_name','email_id','role']
        data = connecsiObj.get__(table_name='users_brands',columns=columns)
        return {'data':data},200

@ns_brand.route('/<string:user_id>')
class Brand(Resource):
    def get(self,user_id):
        '''Brand details by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'first_name', 'last_name', 'company_name', 'email_id', 'role','phone','position','url','country'
                   ,'no_of_employees','city','monthly_budget','business_sector']
        data = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        response_dict = dict(zip(columns, data[0]))
        print(response_dict)
        return {'data':response_dict},200

    @ns_brand.expect(brand_edit_form)
    def put(self,user_id):
        '''Update Brand Details'''
        form_data = request.get_json()
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        phone = form_data.get('phone')
        position = form_data.get('position')
        url = form_data.get('url')
        country = form_data.get('country')
        no_of_employees = form_data.get('no_of_employees')
        city = form_data.get('city')
        monthly_budget = form_data.get('monthly_budget')
        business_sector = form_data.get('business_sector')
        company_name = form_data.get('company_name')
        columns = ['first_name', 'last_name', 'company_name', 'phone', 'position', 'url',
                   'country', 'no_of_employees', 'city', 'monthly_budget', 'business_sector']
        data=(first_name,last_name,company_name,phone,position,url,country,no_of_employees,city,monthly_budget,business_sector)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_brands',columns=columns,WHERE='WHERE',data=data,compare_column='user_id',compare_value=str(user_id))
            return {"response" : 1},200
        except Exception as e:
            return {"response": e},500
