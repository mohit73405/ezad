from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_payments = Namespace('Payments', description='Brand Payments')

brand_payment_form = ns_payments.model('Brand Payments', {
    'amount' : fields.Integer(required=True, description='Amount'),
    'description' : fields.String(required=True, description='Description')
})

@ns_payments.route('/<string:user_id>')
class BrandPayments(Resource):
    @ns_payments.expect(brand_payment_form)
    def post(self,user_id):
        form_data = request.get_json()
        amount = form_data.get('amount')
        description = form_data.get('description')
        connecsiObj = ConnecsiModel()
        columns = ['user_id','email_id']
        data_tuple = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        email_id = data_tuple[0][1]
        data = [user_id, date, email_id, amount, description]
        res = connecsiObj.insert__(table_name='users_brands_payments',
                             columns=['user_id', 'date', 'email_id', 'amount', 'description'], data=data)
        return {'response': res },201

    def get(self,user_id):
        connecsiObj = ConnecsiModel()
        data_tuple = connecsiObj.get__(table_name='users_brands_payments',STAR='*',WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        columns = ["invoice_id", "date", "email_id", "amount", "description"]
        response_list = []
        for item in data_tuple:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list},200

