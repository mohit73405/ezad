from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime



ns_influencer = Namespace('Influencer', description='Influencer Operations')

influencer_register_form = ns_influencer.model('Influencer Details',{
    'channel_id': fields.String(required=True,description='channel id'),
    'business_email': fields.String(required=True,description='Business Email')
})

influencer_edit_form = ns_influencer.model('Influencer Details Update', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'business_email': fields.String(required=True, description='Business Email'),
    'phone': fields.String(required=True, description='Phone'),
    'Categories': fields.String(required=True, description='Categories'),
    'website': fields.String(required=True, description='Website'),
    'country': fields.String(required=True, description='Country'),
    'city': fields.String(required=True, description='City'),
    'social_media_accounts': fields.String(required=True, description='Social Media Accounts')

})


@ns_influencer.route('/<string:user_id>')
class Influencer(Resource):
    def get(self,user_id):
        '''Influencer details by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'first_name', 'last_name', 'company_name', 'email_id', 'role','phone','position','url','country'
                   ,'no_of_employees','city','monthly_budget','business_sector']
        data = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        response_dict = dict(zip(columns, data[0]))
        print(response_dict)
        return {'data':response_dict},200

    @ns_influencer.expect(influencer_edit_form)
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



@ns_influencer.route('/saveInfleuncer')
class Brand(Resource):
    @ns_influencer.expect(influencer_register_form)
    def post(self):
        '''Registers Influencer Details'''
        form_data = request.get_json()
        channel_id= form_data.get('channel_id')
        # password_sha = sha256_crypt.encrypt('influencer123')
        email = form_data.get('business_email')
        columns = ['channel_id','business_email']
        data = [channel_id, email]

        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='users_influencers',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': result},201

        except:
            result=0
            return {'response': result},500

