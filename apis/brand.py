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
        columns = ['user_id', 'first_name', 'last_name', 'company_name', 'email_id', 'role']
        data = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        return {'data':data},200
